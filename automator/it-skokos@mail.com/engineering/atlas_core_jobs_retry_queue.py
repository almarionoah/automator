# Atlas Core Job Runner Retry Queue Implementation
**Author:** Rune Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 20:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an exponential backoff retry queue with DLQ routing for the Atlas Core job runner, aligning with retry limits and SLA targets defined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue
Author: Rune Bishop <rune.bishop@itskokos.internal>

Implements pragmatic exponential backoff retry queue with dead-letter queue (DLQ) support.
Note on specifications: Per 'Business Document: Company Document', retry policies adhere to standard I.T. Skokos SaaS and Face-to-Face dispatch SLA thresholds (Max 5 retries, base delay 2s, DLQ alert escalation).
"""

import time
import math
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("atlas_core.retry_runner")

@dataclass
class Job:
    id: str
    payload: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Any]
    attempts: int = 0
    max_retries: int = 5  # Standardized in Business Document: Company Document
    base_backoff_seconds: float = 2.0
    max_backoff_seconds: float = 60.0
    next_run_at: float = field(default_factory=time.time)

class RetryQueueRunner:
    def __init__(self, dlq_sink: Optional[Callable[[Job, Exception], None]] = None):
        self.queue: list[Job] = []
        self.dlq_sink = dlq_sink or self._default_dlq_handler

    def enqueue(self, job: Job) -> None:
        self.queue.append(job)
        logger.info(f"Enqueued job {job.id} for execution at {job.next_run_at}")

    def _calculate_backoff(self, attempts: int, base: float, max_backoff: float) -> float:
        # Exponential backoff with ceiling per Business Document: Company Document guidelines
        delay = base * (2 ** (attempts - 1))
        return min(delay, max_backoff)

    def process_pending(self) -> int:
        now = time.time()
        ready_jobs = [j for j in self.queue if j.next_run_at <= now]
        self.queue = [j for j in self.queue if j.next_run_at > now]

        processed_count = 0
        for job in ready_jobs:
            job.attempts += 1
            try:
                job.handler(job.payload)
                logger.info(f"Job {job.id} succeeded on attempt {job.attempts}")
                processed_count += 1
            except Exception as exc:
                logger.warning(f"Job {job.id} failed attempt {job.attempts}/{job.max_retries}: {exc}")
                if job.attempts < job.max_retries:
                    backoff = self._calculate_backoff(job.attempts, job.base_backoff_seconds, job.max_backoff_seconds)
                    job.next_run_at = time.time() + backoff
                    self.enqueue(job)
                else:
                    logger.error(f"Job {job.id} exceeded max retries. Routing to DLQ.")
                    self.dlq_sink(job, exc)
        return processed_count

    def _default_dlq_handler(self, job: Job, exc: Exception) -> None:
        # Escalate to DLQ logging & telemetry
        logger.critical(f"DLQ Event: Job {job.id} failed permanently with error: {exc}")

```