# Atlas Core: Graceful Retry Queue Implementation
**Author:** Nova Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 11:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an adaptive retry queue with exponential backoff and user-centered state notifications for Atlas Core job runner, aligning with system resilience and SLA standards in Company Document.

## Deliverable
```
import time
import math
import random
from typing import Callable, Any, Dict
from dataclasses import dataclass

# Design aligned with guidelines defined in Business Document: Company Document
# Emphasizing seamless recovery and transparent UX for background operations.

@dataclass
class JobContext:
    job_id: str
    payload: Dict[str, Any]
    max_retries: int = 5
    base_delay_seconds: float = 1.5
    max_delay_seconds: float = 60.0
    attempt: int = 0
    user_notification_hook: Callable[[str, str], None] = None

class AtlasRetryRunner:
    """
    Job Runner Retry Queue designed for Atlas Core.
    Ensures platform resilience while maintaining a delicate, predictable user experience.
    References Business Document: Company Document for SLA thresholds and backoff multipliers.
    """
    def __init__(self, logger=None):
        self.logger = logger

    def _calculate_backoff(self, attempt: int, base: float, cap: float) -> float:
        # Exponential backoff with full jitter to smooth traffic spikes
        exponential = base * (2 ** attempt)
        delay = min(cap, exponential)
        return random.uniform(0, delay)

    def execute_with_retry(self, ctx: JobContext, task: Callable[[Dict[str, Any]], Any]) -> Any:
        while ctx.attempt < ctx.max_retries:
            try:
                ctx.attempt += 1
                return task(ctx.payload)
            except Exception as exc:
                if ctx.attempt >= ctx.max_retries:
                    if ctx.user_notification_hook:
                        ctx.user_notification_hook(ctx.job_id, "Job paused. We are attending to this.")
                    raise exc
                
                sleep_time = self._calculate_backoff(ctx.attempt, ctx.base_delay_seconds, ctx.max_delay_seconds)
                if ctx.user_notification_hook:
                    ctx.user_notification_hook(ctx.job_id, f"Retrying gently in {round(sleep_time, 1)}s...")
                time.sleep(sleep_time)

```