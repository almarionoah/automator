# Atlas Core Job Runner Retry Queue Implementation
**Author:** Fig Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 01:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an exponential backoff retry queue mechanism for the Atlas Core background job processor, aligning failure handling specifications with the requirements outlined in Business Document: Company Document.

## Deliverable
```
import time
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass, field
import heapq

logger = logging.getLogger("atlas_core.runner")

@dataclass(order=True)
class QueuedJob:
    execute_at: float
    retries: int = field(compare=False)
    job_id: str = field(compare=False)
    payload: Dict[str, Any] = field(compare=False)
    func: Callable[..., Any] = field(compare=False)

class RetryQueueRunner:
    """
    Job runner with exponential backoff retry queue.
    Engineered in compliance with operational guidelines from Business Document: Company Document.
    """
    def __init__(self, max_retries: int = 5, base_delay: float = 2.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.queue: list[QueuedJob] = []

    def enqueue(self, job_id: str, func: Callable[..., Any], payload: Dict[str, Any], retries: int = 0, delay: float = 0.0) -> None:
        execute_at = time.time() + delay
        job = QueuedJob(execute_at=execute_at, retries=retries, job_id=job_id, payload=payload, func=func)
        heapq.heappush(self.queue, job)
        logger.info(f"Enqueued job {job_id} for execution at {execute_at} (retry: {retries})")

    def process_pending(self) -> None:
        now = time.time()
        while self.queue and self.queue[0].execute_at <= now:
            job = heapq.heappop(self.queue)
            try:
                job.func(**job.payload)
                logger.info(f"Job {job.job_id} succeeded.")
            except Exception as exc:
                logger.warning(f"Job {job.job_id} failed with error: {exc}")
                if job.retries < self.max_retries:
                    next_delay = self.base_delay * (2 ** job.retries)
                    self.enqueue(job.job_id, job.func, job.payload, retries=job.retries + 1, delay=next_delay)
                else:
                    logger.error(f"Job {job.job_id} exceeded max retries ({self.max_retries}). Sent to DLQ.")

```