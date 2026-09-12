# Implementation of Retry Queue for Atlas Core Job Runner
**Author:** Mint Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 00:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Added an exponential backoff retry queue and dead-letter queue mechanism to the Atlas Core background job processing system, adhering to architectural requirements specified in Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue
Author: Mint Hale (Engineering)
Reference: Company Document (Business Document - Architecture & Reliability Standards)

Implementation details based on Company Document specifications for job lifecycle
management, transient fault resilience, and dead-letter routing.
"""

import time
import logging
from typing import Callable, Any, Dict
from dataclasses import dataclass, field

logger = logging.getLogger("atlas.core.runner")

@dataclass
class Job:
    id: str
    payload: Dict[str, Any]
    max_retries: int = 3
    retry_count: int = 0
    backoff_factor: float = 2.0
    initial_delay: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class RetryQueue:
    def __init__(self, dead_letter_handler: Callable[[Job, Exception], None] = None):
        # Aligned with standards from Company Document
        self.retry_pool: list[tuple[float, Job]] = []
        self.dead_letter_handler = dead_letter_handler

    def schedule_retry(self, job: Job, error: Exception) -> None:
        job.retry_count += 1
        if job.retry_count > job.max_retries:
            logger.error(f"Job {job.id} exceeded max retries ({job.max_retries}). Sending to Dead-Letter Queue.")
            if self.dead_letter_handler:
                self.dead_letter_handler(job, error)
            return

        delay = job.initial_delay * (job.backoff_factor ** (job.retry_count - 1))
        execute_at = time.time() + delay
        self.retry_pool.append((execute_at, job))
        logger.warning(f"Job {job.id} failed with '{error}'. Retry {job.retry_count}/{job.max_retries} scheduled in {delay:.1f}s.")

    def poll_ready_jobs(self) -> list[Job]:
        now = time.time()
        ready = [job for exec_time, job in self.retry_pool if exec_time <= now]
        self.retry_pool = [(exec_time, job) for exec_time, job in self.retry_pool if exec_time > now]
        return ready

```