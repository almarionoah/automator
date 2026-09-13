# Atlas Core Job Runner: Exponential Backoff & Dead-Letter Retry Queue Implementation
**Author:** Prism Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 22:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements a resilient retry queue module with exponential backoff, jitter, and dead-letter handling for the Atlas Core job runner, aligning with specifications from Business Document: Company Document.

## Deliverable
```
"""
Module: atlas_core.job_runner.retry_queue
Author: Prism Nkosi
Project: Atlas Core

Reference Material:
- Business Document: Company Document (Used to extract operational SLA limits, maximum retry thresholds, and payload serialization compliance rules for I.T. Skokos SaaS and Face-to-Face operations).
"""

import time
import random
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger("atlas_core.retry_queue")

class JobExecutionError(Exception):
    pass

class RetryQueueRunner:
    def __init__(self, max_retries: int = 5, base_delay: float = 1.0, max_delay: float = 60.0):
        # Limits aligned with Business Document: Company Document recovery standards
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.dead_letter_queue = []

    def _calculate_backoff(self, attempt: int) -> float:
        backoff = min(self.max_delay, self.base_delay * (2 ** attempt))
        jitter = random.uniform(0, 0.1 * backoff)  # prevent thundering herd
        return backoff + jitter

    def execute(self, job_id: str, job_fn: Callable[..., Any], payload: Dict[str, Any]) -> Optional[Any]:
        attempt = 0
        while attempt <= self.max_retries:
            try:
                logger.info(f"Executing job {job_id}, attempt {attempt + 1}/{self.max_retries + 1}")
                return job_fn(payload)
            except Exception as exc:
                attempt += 1
                if attempt > self.max_retries:
                    logger.error(f"Job {job_id} exceeded max retries. Moving to DLQ. Error: {exc}")
                    self.dead_letter_queue.append({
                        "job_id": job_id,
                        "payload": payload,
                        "error": str(exc),
                        "timestamp": time.time()
                    })
                    raise JobExecutionError(f"Job {job_id} failed permanently.") from exc
                delay = self._calculate_backoff(attempt)
                logger.warning(f"Job {job_id} failed. Retrying in {delay:.2f}s... (Error: {exc})")
                time.sleep(delay)

```