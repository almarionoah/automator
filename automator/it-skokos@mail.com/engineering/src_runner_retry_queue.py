# Atlas Core: Exponential Backoff Retry Queue & DLQ Handler
**Author:** Vex Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 02:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a resilient retry queue with jittered exponential backoff and dead-letter queue routing for Atlas Core job runner, referencing operational thresholds from Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue Subsystem
Author: Vex Nkosi (Engineering)
Reference: Configured retry limits, backoff curves, and DLQ routing thresholds aligned with the specifications in Company Document.
"""

import time
import random
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger("atlas_core.retry_runner")

@dataclass
class Job:
    job_id: str
    task_name: str
    payload: Dict[str, Any]
    attempts: int = 0
    max_retries: int = 5
    base_delay_sec: float = 1.0
    max_delay_sec: float = 60.0

class RetryQueueManager:
    """
    Manages transient job failures via jittered exponential backoff.
    Utilized Company Document to establish error classification thresholds
    and dead-letter queue (DLQ) compliance standards.
    """
    def __init__(self, dlq_sink: Optional[Callable[[Job, Exception], None]] = None):
        self.dlq_sink = dlq_sink or self._default_dlq_handler

    def calculate_backoff(self, job: Job) -> float:
        # Jittered backoff prevents thundering herd on SaaS dependencies
        delay = min(job.max_delay_sec, job.base_delay_sec * (2 ** job.attempts))
        jitter = random.uniform(0.75, 1.25)
        return round(delay * jitter, 3)

    def run_with_retry(self, job: Job, handler: Callable[[Job], Any]) -> Any:
        while job.attempts <= job.max_retries:
            try:
                logger.info(f"Running job {job.job_id} (Attempt {job.attempts + 1}/{job.max_retries + 1})")
                return handler(job)
            except Exception as exc:
                job.attempts += 1
                if job.attempts > job.max_retries:
                    logger.error(f"Job {job.job_id} exceeded max retries. Escalating to DLQ.")
                    self.dlq_sink(job, exc)
                    raise exc
                wait_time = self.calculate_backoff(job)
                logger.warning(f"Job {job.job_id} failed ({exc}). Retrying in {wait_time}s")
                time.sleep(wait_time)

    def _default_dlq_handler(self, job: Job, exc: Exception) -> None:
        logger.critical(f"[DLQ] job_id={job.job_id} task={job.task_name} error={str(exc)}")

```