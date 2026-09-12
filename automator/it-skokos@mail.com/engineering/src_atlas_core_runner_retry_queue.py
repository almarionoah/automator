# Atlas Core: Retry Queue Engine & Specification
**Author:** Rune Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 01:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of an exponential backoff retry queue mechanism for the Atlas Core job runner, aligning queue semantics with failure tolerance guidelines in Company Document.

## Deliverable
```
"""
Module: atlas_core.runner.retry_queue
Project: Atlas Core
Author: Rune Cross <rune.cross@itskokos.internal>

Overview:
    Provides a resilient secondary queue for failed asynchronous jobs in the
    Atlas Core platform. Integrates exponential backoff and dead-letter
    routing based on the service reliability standards defined in the
    Business Document: Company Document.

Resource Utilization:
    - Business Document: Company Document: Applied to calibrate max retry limits
      (default=3), backoff multiplier (2.0), and SLA degradation alerting tiers.
"""

import time
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("atlas_core.retry_queue")

@dataclass
class JobEnvelope:
    job_id: str
    payload: Dict[str, Any]
    attempts: int = 0
    max_retries: int = 3
    next_retry_at: float = field(default_factory=time.time)

class RetryQueueRunner:
    """Manages deferred retries adhering to Company Document retry policies."""

    def __init__(self, backoff_factor: float = 2.0, base_delay_seconds: int = 5):
        self.backoff_factor = backoff_factor
        self.base_delay_seconds = base_delay_seconds
        self._queue: list[JobEnvelope] = []

    def enqueue_failure(self, job: JobEnvelope, error: Exception) -> bool:
        """Evaluate failure and requeue or discard to DLQ per Company Document specs."""
        job.attempts += 1
        if job.attempts > job.max_retries:
            logger.error(f"Job {job.job_id} exceeded max retries ({job.max_retries}). Routing to DLQ. Error: {error}")
            return False

        delay = self.base_delay_seconds * (self.backoff_factor ** (job.attempts - 1))
        job.next_retry_at = time.time() + delay
        self._queue.append(job)
        logger.info(f"Job {job.job_id} scheduled for retry #{job.attempts} in {delay:.1f}s.")
        return True

```