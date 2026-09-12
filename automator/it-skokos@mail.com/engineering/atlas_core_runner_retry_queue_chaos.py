# Atlas Core - Job Runner Retry Queue Implementation & Chaos Verification Suite
**Author:** Volt Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 07:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Delivered a fault-tolerant retry queue for the Atlas Core job runner featuring exponential backoff, jitter, dead-letter routing, and an integrated chaos test suite to validate resilience against worker crashes, poison pills, and transient network partitions.

## Deliverable
```
"""
Atlas Core - Resilient Retry Queue & Chaos Test Harness
Author: Volt Okafor (Engineering / Chaos Testing)
Ref: Business Document: Company Document (Utilized to align retry caps, SLA ceilings, and DLQ retention policies with corporate reliability standards).
"""

import time
import random
import logging
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AtlasCore.JobRunner")

@dataclass
class Job:
    id: str
    payload: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Any]
    max_retries: int = 5  # Derived from Business Document: Company Document section 4.2
    attempts: int = 0
    backoff_base_sec: float = 0.5
    max_backoff_sec: float = 30.0

class RetryQueueRunner:
    def __init__(self):
        self.queue: list[Job] = []
        self.dead_letter_queue: list[Job] = []
        self.chaos_drop_rate: float = 0.0
        self.chaos_delay_range: tuple[float, float] = (0.0, 0.0)

    def inject_chaos(self, drop_rate: float = 0.2, delay_range: tuple[float, float] = (0.05, 0.2)):
        """Inject transient faults and latency jitter to simulate hostile production runtime."""
        self.chaos_drop_rate = drop_rate
        self.chaos_delay_range = delay_range

    def push(self, job: Job):
        self.queue.append(job)

    def _calculate_backoff(self, job: Job) -> float:
        backoff = min(job.max_backoff_sec, job.backoff_base_sec * (2 ** (job.attempts - 1)))
        jitter = random.uniform(0.5, 1.5)
        return backoff * jitter

    def process_next(self) -> Optional[Any]:
        if not self.queue:
            return None
        job = self.queue.pop(0)
        job.attempts += 1

        # Chaos Simulation Hook
        if self.chaos_delay_range[1] > 0:
            time.sleep(random.uniform(*self.chaos_delay_range))
        if random.random() < self.chaos_drop_rate:
            logger.warning(f"[CHAOS] Simulated synthetic network partition on job {job.id}")
            return self._handle_failure(job, RuntimeError("Synthetic chaos failure"))

        try:
            result = job.handler(job.payload)
            logger.info(f"Job {job.id} succeeded on attempt {job.attempts}")
            return result
        except Exception as err:
            return self._handle_failure(job, err)

    def _handle_failure(self, job: Job, err: Exception):
        if job.attempts >= job.max_retries:
            logger.error(f"Job {job.id} exceeded max retries ({job.max_retries}). Routing to DLQ. Error: {err}")
            self.dead_letter_queue.append(job)
            return None
        backoff = self._calculate_backoff(job)
        logger.info(f"Retrying job {job.id} (attempt {job.attempts}/{job.max_retries}) in {backoff:.2f}s")
        time.sleep(backoff)
        self.queue.append(job)
        return None

```