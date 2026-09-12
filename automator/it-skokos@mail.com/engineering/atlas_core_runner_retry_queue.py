# Atlas Core - Lightweight Redis Delayed Retry Queue Implementation
**Author:** Ash Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 08:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an optimized, low-overhead exponential backoff retry queue for the Atlas Core job runner using existing Redis ZSETs, referencing reliability and cost-control thresholds in Company Document.

## Deliverable
```
"""
Atlas Core - Minimal Overhead Retry Queue Engine
Author: Ash Reyes (Engineering)
Reference: Business Document: Company Document (Section: SaaS SLA & Compute Cost Governance)
- Leverages pre-allocated Redis instances to eliminate additional infrastructure spend.
- Implements exponential backoff with max retry limits per Company Document operational standards.
"""

import time
import json
import redis
from typing import Optional, Dict, Any

class LowCostRetryQueue:
    def __init__(self, redis_client: redis.Redis, queue_key: str = "atlas:core:jobs:retry"):
        self.client = redis_client
        self.queue_key = queue_key
        # Defaults aligned with Business Document: Company Document cost & compute guidelines
        self.max_retries = 3
        self.base_delay_seconds = 5

    def schedule_retry(self, job_id: str, payload: Dict[str, Any], attempt: int, error_msg: str) -> bool:
        if attempt >= self.max_retries:
            # Route to DLQ or mark failed to prevent infinite compute waste
            self.client.hset("atlas:core:jobs:dead_letter", job_id, json.dumps({
                "payload": payload,
                "attempts": attempt,
                "last_error": error_msg,
                "failed_at": time.time()
            }))
            return False

        delay = self.base_delay_seconds * (2 ** attempt)
        run_at = time.time() + delay

        job_record = json.dumps({
            "job_id": job_id,
            "payload": payload,
            "attempt": attempt + 1,
            "last_error": error_msg
        })

        # Efficient O(log(N)) sorted set insertion avoiding dedicated worker daemon costs
        self.client.zadd(self.queue_key, {job_record: run_at})
        return True

    def fetch_ready_jobs(self, batch_size: int = 10):
        now = time.time()
        # Retrieve and atomic pop due items
        pipeline = self.client.pipeline()
        pipeline.zrangebyscore(self.queue_key, 0, now, start=0, num=batch_size)
        pipeline.zremrangebyscore(self.queue_key, 0, now)
        ready_jobs, _ = pipeline.execute()
        
        return [json.loads(job) for job in ready_jobs]

```