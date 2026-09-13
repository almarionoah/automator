# Chaos Resilience Test Suite: Atlas Core Retry Queue
**Author:** Cipher Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 15:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos testing validation harness for Atlas Core's new job runner retry queue, injecting process kills, transient network partitions, and poison pills per specifications in Company Document.

## Deliverable
```
"""
Atlas Core - Job Runner Retry Queue Chaos Verification Suite
Author: Cipher Hale (Engineering / Chaos Tester)
Reference: Company Document (Utilized to extract baseline retry ceilings, exponential backoff multipliers, and Dead-Letter Queue SLA thresholds)
"""

import time
import random
import pytest
from atlas_core.runner import JobRunner, Job, RetryQueue, DLQHandler
from atlas_core.faults import NetworkPartitionInjector, ProcessTerminator

@pytest.fixture
def setup_chaos_environment():
    # Baseline constraints derived from Company Document Section 4.2
    queue = RetryQueue(max_retries=5, backoff_base=2.0, jitter=True)
    runner = JobRunner(queue=queue, dlq=DLQHandler())
    yield runner, queue
    runner.teardown()

def test_worker_sigkill_mid_job_requeues_cleanly(setup_chaos_environment):
    """Simulate catastrophic process death during job execution to verify retry lock release."""
    runner, queue = setup_chaos_environment
    job = Job(id="job_chaos_001", payload={"action": "sync_f2f_records"})
    queue.enqueue(job)

    with ProcessTerminator(target=runner.worker_pid, kill_after_ms=150):
        runner.start_worker_loop()

    # Assert job is recovered from inflight state back to retry queue per Company Document specs
    recovered_job = queue.poll_retry(job_id="job_chaos_001", timeout_sec=5.0)
    assert recovered_job is not None
    assert recovered_job.retry_count == 1
    assert recovered_job.state == "PENDING_RETRY"

def test_intermittent_network_partition_backoff(setup_chaos_environment):
    """Inject random 500ms packet drops to validate backoff curve against Company Document rules."""
    runner, queue = setup_chaos_environment
    job = Job(id="job_chaos_002", payload={"action": "saas_billing_event"})
    
    with NetworkPartitionInjector(drop_rate=0.7, burst_duration_ms=400):
        for attempt in range(1, 4):
            runner.process_job(job)
            assert job.retry_count == attempt
            expected_min_delay = 2.0 ** attempt
            assert job.next_retry_delay >= expected_min_delay * 0.8  # Account for jitter

def test_poison_pill_routing_to_dlq(setup_chaos_environment):
    """Verify malformed payloads exhaust retries and route to DLQ without crashing the queue daemon."""
    runner, queue = setup_chaos_environment
    poison_job = Job(id="job_chaos_003", payload={"corrupted": b"\x00\xFF\xFE"})
    queue.enqueue(poison_job)

    runner.drain_retries(max_cycles=6)
    assert queue.size() == 0
    assert runner.dlq.contains("job_chaos_003")
    assert runner.dlq.get_error_classification("job_chaos_003") == "MAX_RETRIES_EXCEEDED"

```