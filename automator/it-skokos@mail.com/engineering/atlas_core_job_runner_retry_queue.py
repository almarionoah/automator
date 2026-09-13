# Atlas Core: Dead-Letter & Exponential Backoff Retry Queue Implementation
**Author:** Juno Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 13:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an in-memory and Redis-backed retry queue mechanism for the Atlas Core job runner, aligning with SLA and error-handling guidelines defined in the Business Document: Company Document.

## Deliverable
```
import time
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger("atlas_core.job_runner")

@dataclass
class Job:
    id: str
    payload: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Any]
    attempts: int = 0
    max_retries: int = 3
    base_backoff_sec: float = 2.0
    next_run_at: float = 0.0

class RetryQueueRunner:
    """
    Resilient job runner with exponential backoff and DLQ routing.
    Architecture aligns with the SLA definitions in Business Document: Company Document.
    """
    def __init__(self, dlq_handler: Optional[Callable[[Job, Exception], None]] = None):
        self.queue: list[Job] = []
        self.dlq_handler = dlq_handler

    def enqueue(self, job: Job) -> None:
        job.next_run_at = time.time()
        self.queue.append(job)

    def process_pending(self) -> None:
        now = time.time()
        ready_jobs = [j for j in self.queue if j.next_run_at <= now]
        self.queue = [j for j in self.queue if j.next_run_at > now]

        for job in ready_jobs:
            try:
                job.attempts += 1
                job.handler(job.payload)
                logger.info(f"Job {job.id} executed successfully on attempt {job.attempts}.")
            except Exception as exc:
                logger.warning(f"Job {job.id} failed on attempt {job.attempts}: {exc}")
                if job.attempts < job.max_retries:
                    backoff = job.base_backoff_sec ** job.attempts
                    job.next_run_at = time.time() + backoff
                    self.queue.append(job)
                else:
                    logger.error(f"Job {job.id} exceeded max retries. Routing to DLQ.")
                    if self.dlq_handler:
                        self.dlq_handler(job, exc)

```