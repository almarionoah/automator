# Atlas Core: Resilient Job Runner Retry Queue Implementation
**Author:** Rune Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 07:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an empathetic, jittered exponential backoff retry queue for Atlas Core, aligning task recovery with the standards outlined in the Company Document to ensure zero-disruption UX.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue
Author: Rune Reyes (Engineering)
Context: Built in strict accordance with the I.T. Skokos 'Company Document'
         (Service Resiliency & UX Continuity Standards).

Design Philosophy:
A failure in a background worker is a quiet whisper of friction for our users.
We handle retries not merely as computational loops, but as an act of hospitality—
restoring platform harmony before the customer ever feels a stutter.
"""

import time
import random
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("AtlasCore.Runner.RetryQueue")

@dataclass
class JobPayload:
    job_id: str
    task_fn: Callable[..., Any]
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    attempts: int = 0
    max_retries: int = 4
    base_delay_seconds: float = 1.5
    max_delay_seconds: float = 60.0
    context: Dict[str, Any] = field(default_factory=dict)

class RetryQueue:
    def __init__(self, dead_letter_handler: Optional[Callable[[JobPayload, Exception], None]] = None):
        self.dead_letter_handler = dead_letter_handler
        # Aligned with 'Company Document' SLA tolerances for SaaS and Face-to-Face sync workloads
        logger.info("Initialized RetryQueue adhering to Company Document operational resiliency metrics.")

    def calculate_backoff(self, payload: JobPayload) -> float:
        """Exponential backoff with full jitter to preserve system composure."""
        factor = 2 ** payload.attempts
        raw_delay = min(payload.base_delay_seconds * factor, payload.max_delay_seconds)
        return random.uniform(0.5, raw_delay)

    def enqueue_and_run(self, payload: JobPayload) -> Any:
        while payload.attempts <= payload.max_retries:
            try:
                payload.attempts += 1
                logger.debug(f"Executing job {payload.job_id} (Attempt {payload.attempts}/{payload.max_retries + 1})")
                result = payload.task_fn(*payload.args, **payload.kwargs)
                logger.info(f"Job {payload.job_id} completed seamlessly on attempt {payload.attempts}.")
                return result
            except Exception as exc:
                if payload.attempts > payload.max_retries:
                    logger.error(f"Job {payload.job_id} exhausted retries. Invoking graceful dead-letter fallback.")
                    if self.dead_letter_handler:
                        return self.dead_letter_handler(payload, exc)
                    raise exc

                delay = self.calculate_backoff(payload)
                logger.warning(f"Job {payload.job_id} paused due to: {exc}. Preserving UX flow: re-attempting in {delay:.2f}s.")
                time.sleep(delay)

```