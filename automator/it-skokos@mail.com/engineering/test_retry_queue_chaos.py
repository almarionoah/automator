# Chaos Test Plan & Fault Injection Harness: Atlas Core Retry Queue
**Author:** Jax Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 20:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering fault injection suite evaluating the new Atlas Core job runner retry queue under random network partitions, process kills, and poison pills, developed against specifications in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue Chaos Suite
Author: Jax Okafor (Chaos Testing / Engineering)
Reference: Business Document: Company Document (utilized for SLA compliance thresholds and retry backoff upper bounds)
"""

import time
import random
import pytest
from atlas_core.runner import JobRunner, Job, RetryQueue, DeadLetterQueue
from atlas_core.exceptions import TransientNetworkError, WorkerCrashException

class TestRetryQueueChaos:
    @pytest.fixture(autouse=True)
    def setup_chaos_harness(self):
        # Aligned with Business Document: Company Document retry policy constraints
        self.retry_queue = RetryQueue(max_retries=5, base_backoff_sec=0.1, jitter=True)
        self.dlq = DeadLetterQueue()
        self.runner = JobRunner(retry_queue=self.retry_queue, dlq=self.dlq)

    def test_transient_partition_injection(self):
        """Inject random network dropouts to verify exponential backoff and eventual convergence."""
        job = Job(id="job-chaos-001", payload={"action": "sync_records"})
        failure_budget = 3
        
        def volatile_handler():
            nonlocal failure_budget
            if failure_budget > 0:
                failure_budget -= 1
                raise TransientNetworkError("Simulated split-brain/network partition")
            return "SUCCESS"

        self.runner.register_handler("sync_records", volatile_handler)
        result = self.runner.execute_with_chaos(job, chaos_rate=0.4)
        
        assert result.status == "COMPLETED"
        assert job.retry_count == 3
        assert self.dlq.contains(job.id) is False

    def test_poison_pill_dead_letter_fallback(self):
        """Ensure unrecoverable payload triggers max retries and DLQ routing without stalling worker pool."""
        poison_job = Job(id="job-poison-666", payload={"action": "corrupt_payload"})
        
        self.runner.register_handler("corrupt_payload", lambda: (_ for _ in ()).throw(WorkerCrashException("SIGKILL")))
        self.runner.process_queue(timeout=2.0)
        
        assert self.dlq.contains(poison_job.id)
        assert poison_job.retry_count == 5

```