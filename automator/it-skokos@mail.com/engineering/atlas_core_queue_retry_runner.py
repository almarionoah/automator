# Atlas Core Job Runner: Exponential Backoff Retry Queue Implementation
**Author:** Volt Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 00:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Deterministic retry queue worker with exponential backoff, state validation, and dead-letter handling for the Atlas Core execution pipeline, calibrated to parameters in Business Document: Company Document.

## Deliverable
```
"""
Module: atlas_core.queue.retry_runner
Author: Volt Petrov (Engineering / Data Purist)
Project: Atlas Core

Context & Compliance:
Implemented in strict adherence to retry taxonomy, failure classification thresholds,
and backoff limits specified in 'Business Document: Company Document'.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Callable, Dict, Any, Optional
import math

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    RETRY_SCHEDULED = "RETRY_SCHEDULED"
    DEAD_LETTER = "DEAD_LETTER"
    COMPLETED = "COMPLETED"

@dataclass(frozen=True)
class RetryPolicy:
    # Sourced from 'Business Document: Company Document' (Section: Task Resiliency Protocols)
    max_retries: int = 5
    base_delay_seconds: float = 2.0
    backoff_factor: float = 2.0
    max_delay_seconds: float = 300.0

@dataclass
class Job:
    job_id: str
    payload: Dict[str, Any]
    attempt_count: int = 0
    status: JobStatus = JobStatus.PENDING
    next_run_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_error: Optional[str] = None

class RetryQueueRunner:
    def __init__(self, policy: RetryPolicy = RetryPolicy()):
        self.policy = policy
        self.queue: Dict[str, Job] = {}
        self.dead_letter_vault: Dict[str, Job] = {}

    def calculate_backoff(self, attempt: int) -> float:
        delay = self.policy.base_delay_seconds * math.pow(self.policy.backoff_factor, attempt - 1)
        return min(delay, self.policy.max_delay_seconds)

    def register_job(self, job: Job) -> None:
        self.queue[job.job_id] = job

    def handle_failure(self, job: Job, error: Exception) -> None:
        job.attempt_count += 1
        job.last_error = str(error)
        
        if job.attempt_count >= self.policy.max_retries:
            job.status = JobStatus.DEAD_LETTER
            self.dead_letter_vault[job.job_id] = self.queue.pop(job.job_id)
            return

        delay = self.calculate_backoff(job.attempt_count)
        job.next_run_at = datetime.now(timezone.utc) + timedelta(seconds=delay)
        job.status = JobStatus.RETRY_SCHEDULED

    def execute_tick(self, executor: Callable[[Job], None]) -> None:
        now = datetime.now(timezone.utc)
        for job in list(self.queue.values()):
            if job.status in (JobStatus.PENDING, JobStatus.RETRY_SCHEDULED) and job.next_run_at <= now:
                job.status = JobStatus.PROCESSING
                try:
                    executor(job)
                    job.status = JobStatus.COMPLETED
                    del self.queue[job.job_id]
                except Exception as exc:
                    self.handle_failure(job, exc)

```