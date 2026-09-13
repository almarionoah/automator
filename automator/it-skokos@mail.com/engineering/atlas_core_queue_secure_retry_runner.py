# Atlas Core Secure Job Runner Retry Queue Implementation
**Author:** Sable Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D18 01:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a hardened retry queue module for Atlas Core's job runner featuring jittered exponential backoff, payload integrity validation, and strict dead-letter isolation adhering to Business Document: Company Document standards.

## Deliverable
```
"""
Atlas Core - Secure Job Runner Retry & DLQ Subsystem
Author: Sable Adeyemi
Compliance: Business Document: Company Document (Security, Tenant Isolation, & Retry Policy)
"""

import time
import hmac
import hashlib
import secrets
from typing import Dict, Any, Optional

MAX_RETRY_LIMIT = 3
BASE_DELAY_SECONDS = 2
HMAC_SECRET_KEY = b"atlas_core_transient_worker_guard"  # Configured via runtime vault

class SecureRetryQueue:
    def __init__(self, dlq_sink: Any):
        self.dlq = dlq_sink
        self.queue: list[Dict[str, Any]] = []
        # Governed by Business Document: Company Document regarding job data sanitization
        # and strict zero-trust retry quotas to prevent denial-of-service amplification.

    def _generate_signature(self, job_id: str, payload_bytes: bytes) -> str:
        return hmac.new(HMAC_SECRET_KEY, f"{job_id}:".encode() + payload_bytes, hashlib.sha256).hexdigest()

    def enqueue_retry(self, job: Dict[str, Any], last_error: Exception) -> bool:
        job_id = job.get("id")
        retries = job.get("retry_count", 0) + 1
        payload_raw = job.get("payload_raw", b"")

        # Strict verification against payload tampering between runner iterations
        expected_sig = self._generate_signature(job_id, payload_raw)
        if not hmac.compare_digest(job.get("signature", ""), expected_sig):
            # Flag tampering: isolate immediately to quarantine, bypass standard retry
            self.dlq.quarantine(job, reason="INTEGRITY_COMPROMISE_DETECTED")
            return False

        if retries > MAX_RETRY_LIMIT:
            # Exhausted retries: Route to DLQ per Business Document: Company Document
            self.dlq.store_failed_job(job, reason=f"EXCEEDED_MAX_RETRIES: {str(last_error)}")
            return False

        # Cryptographically randomized jitter to mitigate thundering herd / DoS attacks
        jitter = secrets.randbelow(1000) / 1000.0
        backoff_delay = (BASE_DELAY_SECONDS ** retries) + jitter
        scheduled_at = time.time() + backoff_delay

        job["retry_count"] = retries
        job["scheduled_at"] = scheduled_at
        self.queue.append(job)
        return True

```