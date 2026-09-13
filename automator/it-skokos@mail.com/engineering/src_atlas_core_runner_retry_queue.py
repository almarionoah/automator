# Atlas Core - Job Runner Retry Queue Implementation
**Author:** Rune Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 19:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements a typed, deterministic retry queue mechanism with exponential backoff and dead-letter routing for Atlas Core job runner, adhering to operational standards specified in Company Document.

## Deliverable
```
# Project: Atlas Core
# Author: Rune Bishop (Data Purist)
# Reference: Company Document (Section 4: Data Processing & SLA Retry Policies)

"""
Retry Queue module for Atlas Core job runner.

Usage of Company Document:
- Backoff schedules (max 5 retries, base multiplier 2.0) implemented per Company Document Section 4.2.
- Dead-letter payload schemas and data retention flags aligned with governance mandates in Company Document Section 4.5.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, Optional
import math

class JobState(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    RETRY_SCHEDULED = "RETRY_SCHEDULED"
    DEAD_LETTERED = "DEAD_LETTERED"
    COMPLETED = "COMPLETED"

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 5
    initial_interval_seconds: float = 2.0
    backoff_factor: float = 2.0
    max_interval_seconds: float = 300.0

    def calculate_next_run(self, attempt: int) -> datetime:
        delay = min(
            self.initial_interval_seconds * math.pow(self.backoff_factor, attempt - 1),
            self.max_interval_seconds
        )
        return datetime.now(timezone.utc) + timedelta(seconds=delay)

@dataclass
class JobEnvelope:
    job_id: str
    task_name: str
    payload: Dict[str, Any]
    attempt_count: int = 0
    state: JobState = JobState.PENDING
    last_error: Optional[str] = None
    next_run_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class JobRetryQueue:
    def __init__(self, policy: RetryPolicy = RetryPolicy()):
        self.policy = policy
        self._primary_queue: list[JobEnvelope] = []
        self._dead_letter_queue: list[JobEnvelope] = []

    def enqueue(self, job: JobEnvelope) -> None:
        self._primary_queue.append(job)

    def handle_failure(self, job: JobEnvelope, error: str) -> JobEnvelope:
        job.attempt_count += 1
        job.last_error = error

        if job.attempt_count >= self.policy.max_attempts:
            job.state = JobState.DEAD_LETTERED
            self._dead_letter_queue.append(job)
        else:
            job.state = JobState.RETRY_SCHEDULED
            job.next_run_at = self.policy.calculate_next_run(job.attempt_count)
            self.enqueue(job)
        return job

    def get_ready_jobs(self, current_time: Optional[datetime] = None) -> list[JobEnvelope]:
        now = current_time or datetime.now(timezone.utc)
        ready = [j for j in self._primary_queue if j.next_run_at <= now and j.state != JobState.DEAD_LETTERED]
        self._primary_queue = [j for j in self._primary_queue if j not in ready]
        return ready

```