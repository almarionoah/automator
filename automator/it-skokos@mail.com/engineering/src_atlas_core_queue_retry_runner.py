# Atlas Core - Resilient Retry Queue for Job Runner
**Author:** Onyx Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 11:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Atlas Core job runner execution loop to integrate a dedicated retry queue with exponential backoff, jitter, and dead-letter queue (DLQ) support, strictly adhering to reliability standards defined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue Module
Refactored by: Onyx Okafor
Reference: Business Document: Company Document (Retry SLA and Backoff Policy Guidelines)
"""

import time
import math
import random
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("atlas_core.queue")

@dataclass
class Job:
    id: str
    payload: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Any]
    max_retries: int = 5
    attempts: int = 0
    backoff_base: float = 2.0
    next_run_at: float = field(default_factory=time.time)

class RetryQueueRunner:
    def __init__(self, dlq_handler: Optional[Callable[[Job, Exception], None]] = None):
        # Refactored to decouple DLQ pipeline per Business Document: Company Document specs
        self.active_queue: list[Job] = []
        self.retry_queue: list[Job] = []
        self.dlq_handler = dlq_handler

    def enqueue(self, job: Job) -> None:
        self.active_queue.append(job)

    def _calculate_backoff(self, attempts: int, base: float) -> float:
        # Exponential backoff with full jitter as defined in Company Document standards
        raw_delay = math.pow(base, attempts)
        jitter = random.uniform(0.5, 1.5)
        return min(raw_delay * jitter, 300.0)  # Max 5 min cap

    def process_next(self) -> None:
        now = time.time()
        ready_retries = [j for j in self.retry_queue if j.next_run_at <= now]
        for job in ready_retries:
            self.retry_queue.remove(job)
            self.active_queue.append(job)

        if not self.active_queue:
            return

        job = self.active_queue.pop(0)
        try:
            job.attempts += 1
            job.handler(job.payload)
            logger.info(f"Job {job.id} processed successfully.")
        except Exception as exc:
            logger.warning(f"Job {job.id} failed attempt {job.attempts}: {exc}")
            if job.attempts < job.max_retries:
                delay = self._calculate_backoff(job.attempts, job.backoff_base)
                job.next_run_at = time.time() + delay
                self.retry_queue.append(job)
            else:
                logger.error(f"Job {job.id} exceeded max retries. Moving to DLQ.")
                if self.dlq_handler:
                    self.dlq_handler(job, exc)

```