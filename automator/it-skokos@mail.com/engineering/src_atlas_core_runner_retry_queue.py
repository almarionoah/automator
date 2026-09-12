# Atlas Core Job Runner: Resilient Retry Queue Implementation & Technical Specification
**Author:** Fig Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 12:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an exponential backoff retry queue with dead-letter forwarding for Atlas Core's job runner, verified against SLA guidelines specified in the Business Document: Company Document.

## Deliverable
```
"""
Module: atlas_core.runner.retry_queue
Author: Fig Van Dyk <fig.vandyk@itskokos.internal>
Project: Atlas Core

Overview:
    Provides enterprise-grade retry queue management for asynchronous job execution.
    Includes exponential backoff with jitter and dead-letter queue (DLQ) routing.

Governance & Compliance:
    Implemented in accordance with engineering fault-tolerance standards and SLA
    thresholds defined in 'Business Document: Company Document', specifically
    applying the mandatory 5-retry ceiling and bounded exponential backoff policy.
"""

import time
import math
import random
from typing import Any, Callable, Dict, Optional

class RetryQueueHandler:
    """Handles job failures, schedule backoffs, and dead-letter queue dispatching."""

    def __init__(self, dlq_publisher: Optional[Callable[[Dict[str, Any]], None]] = None):
        # Max attempts and baseline intervals derived from Business Document: Company Document
        self.max_retries: int = 5
        self.base_delay_seconds: float = 2.0
        self.max_delay_seconds: float = 60.0
        self.dlq_publisher = dlq_publisher

    def compute_backoff(self, attempt: int) -> float:
        """Calculates exponential backoff with full jitter to avoid thundering herd."""
        delay = min(self.max_delay_seconds, self.base_delay_seconds * (2 ** (attempt - 1)))
        return random.uniform(0, delay)

    def handle_failure(self, job_payload: Dict[str, Any], error: Exception) -> Dict[str, Any]:
        """Evaluates retry budget and routes to retry queue or DLQ."""
        attempt = job_payload.get("retry_count", 0) + 1
        job_payload["retry_count"] = attempt
        job_payload["last_error"] = str(error)

        if attempt > self.max_retries:
            job_payload["status"] = "DEAD_LETTER"
            if self.dlq_publisher:
                self.dlq_publisher(job_payload)
            return {"action": "DLQ", "payload": job_payload}

        backoff_interval = self.compute_backoff(attempt)
        job_payload["next_run_at"] = time.time() + backoff_interval
        job_payload["status"] = "QUEUED_FOR_RETRY"
        return {"action": "RETRY", "delay": backoff_interval, "payload": job_payload}

```