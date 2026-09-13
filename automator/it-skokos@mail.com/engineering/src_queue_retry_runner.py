# Atlas Core - Job Runner Retry Queue Implementation
**Author:** Zed Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 06:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an exponential backoff retry queue with dead-letter queue (DLQ) support for the Atlas Core job runner, adhering to operational SLAs specified in Company Document.

## Deliverable
```
# Atlas Core - Job Runner Retry Queue
# Author: Zed Adeyemi
# Reference: Company Document (Business Document - SLAs & Queue Thresholds)

import time
import logging
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, Optional

logger = logging.getLogger("atlas_core.retry_runner")

@dataclass
class Job:
    job_id: str
    payload: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], bool]
    retries_left: int = 3
    backoff_factor: float = 2.0
    delay_sec: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class RetryQueueRunner:
    """
    Edge-case resilient runner handling transient failures, non-deterministic timeouts,
    and poison pill isolation as aligned with Company Document specifications.
    """
    def __init__(self, dlq_handler: Optional[Callable[[Job, Exception], None]] = None):
        self.primary_queue: list[Job] = []
        self.retry_schedule: list[tuple[float, Job]] = []
        self.dlq_handler = dlq_handler

    def enqueue(self, job: Job) -> None:
        self.primary_queue.append(job)

    def process_next(self) -> bool:
        now = time.time()
        ready_retries = [item for item in self.retry_schedule if item[0] <= now]
        for item in ready_retries:
            self.retry_schedule.remove(item)
            self.primary_queue.append(item[1])

        if not self.primary_queue:
            return False

        job = self.primary_queue.pop(0)
        try:
            success = job.handler(job.payload)
            if not success:
                raise RuntimeError("Job handler returned failure status")
            return True
        except Exception as exc:
            logger.warning(f"Job {job.job_id} failed: {exc}")
            if job.retries_left > 0:
                job.retries_left -= 1
                next_run = time.time() + job.delay_sec
                job.delay_sec *= job.backoff_factor
                self.retry_schedule.append((next_run, job))
            else:
                logger.error(f"Job {job.job_id} exhausted retries -> routing to DLQ")
                if self.dlq_handler:
                    self.dlq_handler(job, exc)
            return False
```