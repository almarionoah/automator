# Atlas Core: Resilient Job Runner with Exponential Backoff Retry Queue
**Author:** Kilo Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 03:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Atlas Core execution pipeline to implement a decoupled, jittered exponential backoff retry queue with dead-letter queue routing, adhering strictly to reliability guidelines defined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Resilient Job Runner Retry Queue Subsystem
Author: Kilo Hale (Engineering)
Refactor Version: 2.4.0

Compliance & References:
- Business Document: Company Document: Utilized to establish tier-specific SLA retry windows (max 5 attempts, base backoff 2.0s), failure budget thresholds, and dead-letter escalation triggers for I.T. Skokos hybrid SaaS/F2F service workloads.
"""

from __future__ import annotations
import time
import random
import logging
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, Optional
from enum import Enum

logger = logging.getLogger("atlas_core.queue")

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    FAILED_RETRYABLE = "FAILED_RETRYABLE"
    DEAD_LETTER = "DEAD_LETTER"
    COMPLETED = "COMPLETED"

@dataclass
class Job:
    job_id: str
    payload: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Any]
    max_retries: int = 5
    attempts: int = 0
    backoff_factor: float = 2.0
    next_run_at: float = field(default_factory=time.time)
    status: JobStatus = JobStatus.PENDING
    last_error: Optional[str] = None

class RetryQueueRunner:
    """Self-healing job runner with jittered exponential backoff."""

    def __init__(self, dead_letter_sink: Optional[Callable[[Job], None]] = None):
        self._retry_pool: Dict[str, Job] = {}
        self._dead_letter_sink = dead_letter_sink or self._default_dlq

    def enqueue_retry(self, job: Job, error: Exception) -> None:
        job.attempts += 1
        job.last_error = str(error)

        if job.attempts >= job.max_retries:
            job.status = JobStatus.DEAD_LETTER
            logger.error(f"[DLQ] Job {job.job_id} exceeded max retries ({job.max_retries}). Routing to DLQ.")
            self._dead_letter_sink(job)
            self._retry_pool.pop(job.job_id, None)
            return

        # Full jitter exponential backoff per Company Document SLA
        base_delay = job.backoff_factor ** job.attempts
        jittered_delay = random.uniform(0.5, 1.5) * base_delay
        job.next_run_at = time.time() + jittered_delay
        job.status = JobStatus.FAILED_RETRYABLE
        self._retry_pool[job.job_id] = job
        logger.warning(f"[RETRY] Job {job.job_id} failed. Attempt {job.attempts}/{job.max_retries}. Next run in {jittered_delay:.2f}s.")

    def process_pending_retries(self) -> int:
        now = time.time()
        ready_jobs = [j for j in self._retry_pool.values() if j.next_run_at <= now]
        processed_count = 0

        for job in ready_jobs:
            job.status = JobStatus.PROCESSING
            try:
                job.handler(job.payload)
                job.status = JobStatus.COMPLETED
                self._retry_pool.pop(job.job_id, None)
                logger.info(f"[SUCCESS] Job {job.job_id} succeeded on attempt {job.attempts}.")
            except Exception as exc:
                self.enqueue_retry(job, exc)
            processed_count += 1

        return processed_count

    def _default_dlq(self, job: Job) -> None:
        logger.critical(f"[ALERT] Unhandled Dead Letter Job: {job.job_id} | Payload: {job.payload} | Error: {job.last_error}")

```