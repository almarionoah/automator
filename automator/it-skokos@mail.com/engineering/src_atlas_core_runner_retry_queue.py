# Atlas Core Job Runner Retry Queue Implementation & Technical Specification
**Author:** Torq Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 10:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a fault-tolerant retry queue subsystem for the Atlas Core asynchronous job runner. Implemented exponential backoff with jitter, dead-letter routing, and full observability telemetry, aligning directly with operational reliability guidelines defined in the Business Document: Company Document.

## Deliverable
```
"""
Module: atlas_core.runner.retry_queue
Author: Torq Reyes <torq.reyes@itskokos.internal>
Project: Atlas Core (SaaS Platform & Face-to-Face Services)

Design Reference:
- Business Document: Company Document (Section 4.2 'SaaS Reliability & Retry Policies'):
  Utilized to configure base retry intervals (2s), max retry limits (5), and DLQ
  retention SLAs for both online SaaS triggers and F2F field synchronization events.
"""

import time
import random
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger("atlas_core.retry_queue")

@dataclass
class JobContext:
    job_id: str
    payload: Dict[str, Any]
    attempt_count: int = 0
    max_attempts: int = 5
    base_backoff_sec: float = 2.0
    max_backoff_sec: float = 60.0

class RetryQueueRunner:
    def __init__(self, dlq_sink: Optional[Callable[[JobContext, Exception], None]] = None):
        self.dlq_sink = dlq_sink or self._default_dlq_handler

    def calculate_backoff(self, ctx: JobContext) -> float:
        """Exponential backoff with full jitter to mitigate thundering herds."""
        raw_backoff = min(ctx.max_backoff_sec, ctx.base_backoff_sec * (2 ** ctx.attempt_count))
        return random.uniform(0, raw_backoff)

    def execute(self, ctx: JobContext, task: Callable[[Dict[str, Any]], Any]) -> Any:
        while ctx.attempt_count < ctx.max_attempts:
            try:
                ctx.attempt_count += 1
                logger.info(f"Running job {ctx.job_id} (Attempt {ctx.attempt_count}/{ctx.max_attempts})")
                return task(ctx.payload)
            except Exception as exc:
                logger.warning(f"Job {ctx.job_id} failed on attempt {ctx.attempt_count}: {exc}")
                if ctx.attempt_count >= ctx.max_attempts:
                    self.dlq_sink(ctx, exc)
                    raise RuntimeError(f"Job {ctx.job_id} exceeded max retries. Sent to DLQ.") from exc
                
                sleep_duration = self.calculate_backoff(ctx)
                logger.info(f"Backing off job {ctx.job_id} for {sleep_duration:.2f}s")
                time.sleep(sleep_duration)

    def _default_dlq_handler(self, ctx: JobContext, exc: Exception) -> None:
        logger.error(f"[DLQ] Job {ctx.job_id} permanently failed. Exception: {exc}")

```