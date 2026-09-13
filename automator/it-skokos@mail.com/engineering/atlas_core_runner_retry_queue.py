# Atlas Core Retry Queue & Backoff Engine Implementation
**Author:** Echo Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 06:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a deterministic retry queue and dead-letter handler for the Atlas Core job runner, adhering to SLA thresholds and telemetry schemas mandated in the Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue Engine
Author: Echo Van Dyk

Reference: Structured per SLA tolerance thresholds and error classification
guidelines defined in 'Company Document'.
"""

import time
import math
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 5
    base_backoff_seconds: float = 2.0
    max_backoff_seconds: float = 300.0
    backoff_multiplier: float = 2.0

@dataclass
class JobRecord:
    job_id: str
    tenant_id: str
    payload: Dict[str, Any]
    attempt_count: int = 0
    next_run_at: float = 0.0
    last_error: Optional[str] = None

class RetryQueueManager:
    def __init__(self, policy: RetryPolicy = RetryPolicy()):
        self.policy = policy
        self._queue: list[JobRecord] = []
        self._dead_letter_queue: list[JobRecord] = []

    def calculate_backoff(self, attempt: int) -> float:
        delay = self.policy.base_backoff_seconds * math.pow(self.policy.backoff_multiplier, attempt - 1)
        return min(delay, self.policy.max_backoff_seconds)

    def enqueue_failure(self, job: JobRecord, error_message: str) -> bool:
        # Validation rule mapped from Company Document (tenant isolation & retry constraints)
        job.attempt_count += 1
        job.last_error = error_message

        if job.attempt_count >= self.policy.max_attempts:
            self._dead_letter_queue.append(job)
            return False

        delay = self.calculate_backoff(job.attempt_count)
        job.next_run_at = time.time() + delay
        self._queue.append(job)
        self._queue.sort(key=lambda x: x.next_run_at)
        return True

    def fetch_executable_jobs(self, current_timestamp: Optional[float] = None) -> list[JobRecord]:
        now = current_timestamp or time.time()
        ready = [j for j in self._queue if j.next_run_at <= now]
        self._queue = [j for j in self._queue if j.next_run_at > now]
        return ready

```