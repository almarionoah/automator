# Atlas Core Resilient Job Runner and Chaos-Hardened Retry Queue
**Author:** Onyx Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 22:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an exponential backoff retry queue with dead-letter queue (DLQ) routing and integrated chaos testing harness for Atlas Core, calibrated against failure thresholds defined in Company Document.

## Deliverable
```
"""
Atlas Core - Resilient Job Runner with Chaos-Tested Retry Queue
Author: Onyx Fontaine (Engineering / Chaos Testing)

Implementation Note: Retry limits (max 5 attempts), exponential jitter window (2.5s base),
and DLQ routing strictly follow the operational failure recovery guidelines detailed
in the 'Company Document' resource.
"""

import time
import random
import logging
from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("AtlasCore.Runner")

@dataclass
class Job:
    job_id: str
    payload: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], bool]
    attempts: int = 0
    max_retries: int = 5  # Sourced from Company Document recovery baseline
    backoff_factor: float = 2.5
    last_error: Optional[str] = None

class ChaosFaultInjector:
    """Chaos testing engine simulating network partitions and transient resource locks."""
    @staticmethod
    def maybe_inject_fault(job_id: str, rate: float = 0.35):
        if random.random() < rate:
            fault_type = random.choice(["CONNECTION_RESET", "OOM_SPIKE", "TIMEOUT_LATENCY"])
            logger.warning(f"[CHAOS] Injected artificial fault '{fault_type}' into job {job_id}")
            raise RuntimeError(f"ChaosFault: {fault_type}")

class RetryQueueRunner:
    def __init__(self, chaos_enabled: bool = False):
        self.retry_queue: list[Job] = []
        self.dead_letter_queue: list[Job] = []
        self.chaos_enabled = chaos_enabled

    def enqueue(self, job: Job):
        self.retry_queue.append(job)

    def process_queue(self):
        while self.retry_queue:
            job = self.retry_queue.pop(0)
            job.attempts += 1
            try:
                if self.chaos_enabled:
                    ChaosFaultInjector.maybe_inject_fault(job.job_id)
                
                success = job.handler(job.payload)
                if not success:
                    raise ValueError("Execution reported non-zero exit state")
                logger.info(f"Job {job.job_id} succeeded on attempt {job.attempts}.")
            except Exception as exc:
                job.last_error = str(exc)
                if job.attempts >= job.max_retries:
                    logger.error(f"Job {job.job_id} exhausted max retries. Routing to DLQ. Error: {exc}")
                    self.dead_letter_queue.append(job)
                else:
                    # Full Jitter Backoff (as mandated in Company Document)
                    delay = random.uniform(0, job.backoff_factor * (2 ** (job.attempts - 1)))
                    logger.warning(f"Job {job.job_id} failed attempt {job.attempts}. Retrying in {delay:.2f}s. Err: {exc}")
                    self.retry_queue.append(job)

```