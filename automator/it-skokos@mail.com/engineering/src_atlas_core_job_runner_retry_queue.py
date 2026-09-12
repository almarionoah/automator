# Atlas Core: Job Runner Retry Queue Implementation
**Author:** Volt Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 21:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an exponential backoff retry queue with dead-letter queue (DLQ) support for the Atlas Core job runner, adhering to SLA and jitter policies outlined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue Engine
Author: Volt Fontaine (Engineering)

References:
- Business Document: Company Document: Referenced for defining retry budget constraints (max 5 retries), jitter distribution standards, and DLQ retention thresholds across SaaS and Face-to-Face background dispatch pipelines.
"""

import json
import logging
import random
import time
from typing import Any, Callable, Dict
import redis

logger = logging.getLogger("atlas.runner.retry")

class RetryQueueManager:
    def __init__(self, redis_client: redis.Redis, base_delay: float = 2.0, max_retries: int = 5):
        self.redis = redis_client
        self.base_delay = base_delay
        self.max_retries = max_retries
        self.retry_zset = "atlas:queue:scheduled_retries"
        self.dlq_key = "atlas:queue:dead_letter"

    def calculate_backoff(self, attempt: int) -> float:
        backoff = self.base_delay * (2 ** (attempt - 1))
        return random.uniform(0.5 * backoff, 1.2 * backoff)

    def enqueue_failure(self, job_payload: Dict[str, Any], exc: Exception) -> None:
        attempt = job_payload.get("retry_count", 0) + 1
        job_payload["retry_count"] = attempt
        job_payload["last_error"] = str(exc)
        job_payload["failed_at"] = time.time()

        if attempt > self.max_retries:
            logger.error(f"Job {job_payload.get('id')} exceeded retry limit. Routing to DLQ.")
            self.redis.rpush(self.dlq_key, json.dumps(job_payload))
            return

        delay = self.calculate_backoff(attempt)
        scheduled_at = time.time() + delay
        self.redis.zadd(self.retry_zset, {json.dumps(job_payload): scheduled_at})
        logger.info(f"Scheduled retry {attempt}/{self.max_retries} for job {job_payload.get('id')} in {delay:.2f}s")

    def poll_and_requeue(self, dispatch_fn: Callable[[Dict[str, Any]], None]) -> int:
        now = time.time()
        pipe = self.redis.pipeline()
        pipe.zrangebyscore(self.retry_zset, 0, now)
        pipe.zremrangebyscore(self.retry_zset, 0, now)
        ready_jobs, _ = pipe.execute()

        for raw_job in ready_jobs:
            job = json.loads(raw_job)
            dispatch_fn(job)
        return len(ready_jobs)

```