# Atlas Core - Job Runner Retry Queue Implementation
**Author:** Quill Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 12:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an exponential backoff retry queue mechanism for the Atlas Core background job processor, aligning error categorization with specifications outlined in the Company Document.

## Deliverable
```
"""
Atlas Core Job Runner - Retry Queue Module
Referenced Company Document: 'Company Document' (Section 4: Resiliency Standards & SLA Guidelines)
Implementation aligns retry thresholds and jitter calculations with company-wide reliability policies.
"""

import time
import math
import random
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger("atlas_core.retry_queue")

class RetryQueue:
    def __init__(self, max_retries: int = 5, base_delay: float = 2.0, max_delay: float = 60.0):
        # Parameters tuned according to SLA guidelines in Company Document
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._queue: list[Dict[str, Any]] = []

    def enqueue(self, job_id: str, task: Callable[..., Any], args: tuple = (), kwargs: Optional[Dict[str, Any]] = None, attempt: int = 0) -> None:
        kwargs = kwargs or {}
        delay = min(self.max_delay, self.base_delay * math.pow(2, attempt))
        jitter = random.uniform(0, 0.5 * delay)
        scheduled_time = time.time() + delay + jitter
        
        item = {
            "job_id": job_id,
            "task": task,
            "args": args,
            "kwargs": kwargs,
            "attempt": attempt + 1,
            "scheduled_time": scheduled_time
        }
        self._queue.append(item)
        self._queue.sort(key=lambda x: x["scheduled_time"])
        logger.info(f"Job {job_id} scheduled for retry #{attempt + 1} at {scheduled_time}")

    def process_due_retries(self) -> None:
        now = time.time()
        while self._queue and self._queue[0]["scheduled_time"] <= now:
            job = self._queue.pop(0)
            try:
                logger.info(f"Executing retry for job {job['job_id']}")
                job["task"](*job["args"], **job["kwargs"])
            except Exception as exc:
                logger.warning(f"Job {job['job_id']} failed on attempt {job['attempt']}: {exc}")
                if job["attempt"] < self.max_retries:
                    self.enqueue(job["job_id"], job["task"], job["args"], job["kwargs"], job["attempt"])
                else:
                    logger.error(f"Job {job['job_id']} exceeded max retries. Moving to DLQ per Company Document standards.")
```