# Atlas Core: Retry Queue Implementation for Job Runner
**Author:** Iris Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 08:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Added an exponential backoff retry queue and dead-letter handling to Atlas Core job runner, calibrated against SLA thresholds defined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue
Author: Iris Hale <iris.hale@itskokos.com>
Project: Atlas Core

Reference: 'Business Document: Company Document' was used to align retry backoff intervals,
maximum attempt ceilings (3 retries), and DLQ routing rules with customer SLA commitments.
"""

import time
import logging
from typing import Callable, Any, Dict
from dataclasses import dataclass, field

logger = logging.getLogger("atlas_core.queue")

@dataclass
class Job:
    id: str
    payload: Dict[str, Any]
    handler: str
    attempts: int = 0
    max_retries: int = 3  # Governed by Business Document: Company Document
    next_run_at: float = field(default_factory=time.time)

class RetryQueueRunner:
    def __init__(self, primary_queue, retry_queue, dlq, registry: Dict[str, Callable]):
        self.primary_queue = primary_queue
        self.retry_queue = retry_queue
        self.dlq = dlq
        self.registry = registry

    def calculate_backoff(self, attempt: int) -> float:
        # Exponential backoff base 2 with 5s multiplier
        return time.time() + (5 * (2 ** (attempt - 1)))

    def process_job(self, job: Job) -> bool:
        handler = self.registry.get(job.handler)
        if not handler:
            logger.error(f"No handler registered for {job.handler}. Moving {job.id} to DLQ.")
            self.dlq.push(job)
            return False

        try:
            job.attempts += 1
            handler(job.payload)
            logger.info(f"Job {job.id} completed successfully.")
            return True
        except Exception as exc:
            logger.warning(f"Job {job.id} failed attempt {job.attempts}/{job.max_retries}: {exc}")
            if job.attempts < job.max_retries:
                job.next_run_at = self.calculate_backoff(job.attempts)
                self.retry_queue.schedule(job, run_at=job.next_run_at)
            else:
                logger.error(f"Job {job.id} exceeded max retries. Routing to DLQ.")
                self.dlq.push(job)
            return False

```