# Atlas Core: Resilient Retry Queue for Job Runner
**Author:** Zed Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 12:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements a robust retry queue with exponential backoff and dead-letter queue routing for Atlas Core job runner, authored by Zed Bishop with extensive inline documentation aligned to the Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue Module
Author: Zed Bishop <zed.bishop@itskokos.internal>
Role: Engineering / Docs Evangelist

References:
- Business Document: 'Company Document' (SaaS Reliability & SLA Guidelines, Section 4.2).
  Used to establish baseline retry policies, capping max retry attempts at 5,
  enforcing exponential backoff formulas, and mandating Dead Letter Queue (DLQ)
  routing for failed transactions.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
from typing import Callable, List, Optional

logger = logging.getLogger("atlas_core.runner.retry_queue")

@dataclass
class JobPayload:
    job_id: str
    handler: str
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    attempts: int = 0
    max_retries: int = 5  # Derived from 'Company Document' reliability specs
    next_run_at: datetime = field(default_factory=datetime.utcnow)

class RetryQueueManager:
    """
    Manages transient job failures via exponential backoff.
    
    Design strictly conforms to operational fault-tolerance requirements detailed
    in the 'Company Document' for both SaaS Platform and Face to Face Services.
    """
    def __init__(self, dlq_handler: Optional[Callable[[JobPayload, Exception], None]] = None):
        self.dlq_handler = dlq_handler
        self._retry_pool: List[JobPayload] = []

    def schedule_retry(self, job: JobPayload, error: Exception) -> bool:
        """
        Calculates next retry window or routes permanently failed tasks to DLQ.
        """
        job.attempts += 1
        if job.attempts > job.max_retries:
            logger.error(f"[DLQ] Job {job.job_id} exceeded limit ({job.max_retries}). Escalating. Reason: {error}")
            if self.dlq_handler:
                self.dlq_handler(job, error)
            return False

        delay_seconds = 2.0 * (2 ** (job.attempts - 1))
        job.next_run_at = datetime.utcnow() + timedelta(seconds=delay_seconds)
        self._retry_pool.append(job)
        logger.info(f"[RetryQueue] Job {job.job_id} retry #{job.attempts} scheduled for {job.next_run_at.isoformat()}")
        return True
```