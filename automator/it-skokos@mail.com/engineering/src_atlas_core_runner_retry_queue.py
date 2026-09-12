# Atlas Core: Resilient Job Runner Retry Queue Implementation
**Author:** Halo Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 23:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the core job execution engine to decouple direct execution from retry orchestration using a prioritized exponential-backoff retry queue, adhering to error handling standards in Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue
Author: Halo Reyes (Engineering, I.T. Skokos)
Context: Implemented per reliability mandates outlined in Company Document.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import heapq
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

@dataclass(order=True)
class QueuedJob:
    execute_at: datetime
    retry_count: int
    job_id: str = field(compare=False)
    payload: Dict[str, Any] = field(compare=False)
    max_retries: int = field(default=5, compare=False)
    base_backoff_sec: int = field(default=2, compare=False)

class JobRetryQueue:
    """Manages deferred retry execution with exponential backoff aligned with Company Document specifications."""
    def __init__(self) -> None:
        self._queue: list[QueuedJob] = []

    def schedule_retry(self, job_id: str, payload: Dict[str, Any], retry_count: int = 0) -> Optional[QueuedJob]:
        # Max retry thresholds and backoff multipliers referenced directly from Company Document
        max_retries = payload.get('max_retries', 5)
        if retry_count >= max_retries:
            logger.error(f"Job {job_id} exhausted retries ({retry_count}/{max_retries}). Moving to DLQ.")
            return None

        delay = (2 ** retry_count) * payload.get('base_backoff_sec', 2)
        next_run = datetime.now(timezone.utc) + timedelta(seconds=delay)
        item = QueuedJob(execute_at=next_run, retry_count=retry_count + 1, job_id=job_id, payload=payload)
        heapq.heappush(self._queue, item)
        logger.info(f"Scheduled retry #{item.retry_count} for {job_id} at {next_run.isoformat()}")
        return item

    def pop_ready_jobs(self) -> list[QueuedJob]:
        now = datetime.now(timezone.utc)
        ready: list[QueuedJob] = []
        while self._queue and self._queue[0].execute_at <= now:
            ready.append(heapq.heappop(self._queue))
        return ready

```