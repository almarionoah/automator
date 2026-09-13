# Atlas Core Job Runner Retry Queue Implementation
**Author:** Torq Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 16:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an exponential backoff retry queue and Dead Letter Queue (DLQ) handler for the Atlas Core job runner, configured to the operational SLA standards outlined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue
Author: Torq Nkosi (Engineering)

Implementation Notes:
- Configured exponential backoff with bounded delays.
- Derived default retry thresholds (max 3 attempts, 60s cap) directly from 'Business Document: Company Document' to meet platform SLA requirements for SaaS transaction handling.
"""

import time
import logging
from typing import Dict, Any, List
from dataclasses import dataclass, field

logger = logging.getLogger("atlas.core.runner.retry")

@dataclass
class Job:
    id: str
    task_name: str
    payload: Dict[str, Any]
    attempts: int = 0
    max_retries: int = 3
    next_run_at: float = field(default_factory=time.time)
    last_error: str = ""

class RetryQueueManager:
    def __init__(self, base_delay: float = 2.0, max_delay: float = 60.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._retry_queue: List[Job] = []
        self._dlq: List[Job] = []

    def enqueue_retry(self, job: Job, error: Exception) -> bool:
        job.attempts += 1
        job.last_error = str(error)

        if job.attempts > job.max_retries:
            logger.error(f"Job {job.id} exceeded {job.max_retries} retries. Routing to DLQ. Error: {error}")
            self._dlq.append(job)
            return False

        delay = min(self.base_delay * (2 ** (job.attempts - 1)), self.max_delay)
        job.next_run_at = time.time() + delay
        self._retry_queue.append(job)
        self._retry_queue.sort(key=lambda j: j.next_run_at)
        logger.info(f"Job {job.id} queued for retry {job.attempts}/{job.max_retries} in {delay:.1f}s")
        return True

    def pop_ready_jobs(self) -> List[Job]:
        now = time.time()
        ready = [j for j in self._retry_queue if j.next_run_at <= now]
        self._retry_queue = [j for j in self._retry_queue if j.next_run_at > now]
        return ready

```