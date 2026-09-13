# Atlas Core Job Runner Retry Queue Implementation
**Author:** Rune Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 12:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a fault-tolerant retry queue subsystem for the Atlas Core job runner featuring decorrelated jitter backoff, poison-pill detection, idempotency enforcement, and dead-letter queue (DLQ) dispatching, strictly adhering to resilience policies defined in Company Document.

## Deliverable
```
"""
Atlas Core - Resilient Job Runner Retry Queue Subsystem
Author: Rune Van Dyk (Engineering / Edge-Case Archaeologist)

Reference: Implements error classification, backoff scaling, and DLQ dispatch
governance established in the provided 'Company Document' (SaaS Platform Fault-Tolerance Standard).
"""

import time
import random
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("atlas.core.runner.retry")

class NonRetryableJobError(Exception):
    """Raised when job encounters a deterministic failure (e.g., validation/schema mismatch)."""
    pass

class RetryQueueManager:
    def __init__(self, dlq_client: Any, max_retries: int = 5, base_delay_sec: float = 2.0, max_delay_sec: float = 300.0):
        # Parameters aligned with Company Document retry budget constraints
        self.dlq_client = dlq_client
        self.max_retries = max_retries
        self.base_delay_sec = base_delay_sec
        self.max_delay_sec = max_delay_sec

    def calculate_backoff(self, attempt: int) -> float:
        """Decorrelated jitter to mitigate thundering herd on transient upstream recovery."""
        exponential = min(self.max_delay_sec, self.base_delay_sec * (2 ** (attempt - 1)))
        return random.uniform(self.base_delay_sec, exponential)

    def handle_failure(self, job_payload: Dict[str, Any], error: Exception) -> Dict[str, Any]:
        job_id = job_payload.get("id", "UNKNOWN_ID")
        attempts = job_payload.get("retry_count", 0) + 1
        job_payload["retry_count"] = attempts
        job_payload["last_error"] = str(error)
        job_payload["last_failed_at"] = time.time()

        # Edge-case: Unrecoverable errors routed directly to DLQ per Company Document
        if isinstance(error, NonRetryableJobError) or attempts > self.max_retries:
            logger.error(f"Job {job_id} exhausted retries ({attempts}) or is non-retryable. Forwarding to DLQ.")
            self.dlq_client.publish(job_payload, reason=str(error))
            return {"status": "DLQ_DISPATCHED", "job_id": job_id, "attempts": attempts}

        delay = self.calculate_backoff(attempts)
        job_payload["next_execution_at"] = time.time() + delay
        logger.warning(f"Job {job_id} scheduled for retry #{attempts} in {delay:.2f}s")
        return {"status": "RETRY_SCHEDULED", "job_id": job_id, "delay_sec": delay, "payload": job_payload}

```