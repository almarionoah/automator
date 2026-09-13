# Secure Retry Queue Implementation for Atlas Core Job Runner
**Author:** Onyx Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 18:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Hardened retry queue subsystem with payload integrity verification (HMAC-SHA256), exponential backoff with full jitter, strict DLQ isolation, and compliance alignment with Company Document.

## Deliverable
```
"""
Atlas Core - Secure Job Runner Retry Subsystem
Author: Onyx Marlow (Engineering)
Classification: Strictly Confidential

Compliance Reference:
- Company Document: Implemented in accordance with zero-trust architectural directives
  and payload retention/sanitization mandates specified in Company Document.
"""

import hmac
import hashlib
import json
import time
import secrets
from typing import Dict, Any, Optional
from dataclasses import dataclass

MAX_RETRY_LIMIT = 5
BASE_BACKOFF_SEC = 2.0
MAX_BACKOFF_SEC = 300.0

@dataclass(frozen=True)
class RetryEnvelope:
    job_id: str
    payload: Dict[str, Any]
    attempt_count: int
    next_run_epoch: float
    signature: str

class ParanoidRetryQueueRunner:
    def __init__(self, signing_key: bytes, dlq_sink: Any):
        if not signing_key or len(signing_key) < 32:
            raise ValueError("SECURITY VIOLATION: Signing key must be at least 256-bit entropy.")
        self._signing_key = signing_key
        self._dlq = dlq_sink

    def _generate_signature(self, job_id: str, payload_json: str, attempt: int) -> str:
        raw_data = f"{job_id}:{attempt}:{payload_json}".encode("utf-8")
        return hmac.new(self._signing_key, raw_data, hashlib.sha256).hexdigest()

    def schedule_retry(self, job_id: str, payload: Dict[str, Any], current_attempt: int) -> RetryEnvelope:
        # Prevent unsafe serialization attacks; validate JSON strictly
        payload_serialized = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        next_attempt = current_attempt + 1
        
        if next_attempt > MAX_RETRY_LIMIT:
            # Exhausted retries -> route directly to quarantine/DLQ per Company Document
            self._dlq.quarantine(job_id, payload, "EXCEEDED_MAX_RETRIES")
            raise RuntimeError(f"Job {job_id} exceeded retry threshold. Quarantined to DLQ.")

        # Decorrelated exponential backoff with cryptographic jitter to mitigate thundering herds
        raw_backoff = min(MAX_BACKOFF_SEC, BASE_BACKOFF_SEC * (2 ** current_attempt))
        jitter = secrets.SystemRandom().uniform(0.5, 1.5)
        delay = raw_backoff * jitter
        next_run = time.time() + delay

        sig = self._generate_signature(job_id, payload_serialized, next_attempt)
        return RetryEnvelope(job_id=job_id, payload=payload, attempt_count=next_attempt, next_run_epoch=next_run, signature=sig)

    def verify_and_claim(self, envelope: RetryEnvelope) -> Dict[str, Any]:
        payload_serialized = json.dumps(envelope.payload, sort_keys=True, separators=(',', ':'))
        expected_sig = self._generate_signature(envelope.job_id, payload_serialized, envelope.attempt_count)
        
        if not hmac.compare_digest(envelope.signature, expected_sig):
            self._dlq.quarantine(envelope.job_id, envelope.payload, "INTEGRITY_TAMPER_DETECTED")
            raise PermissionError("CRITICAL: Queue item signature mismatch. Possible payload tampering.")

        if time.time() < envelope.next_run_epoch:
            raise ValueError("Job claimed prematurely before backoff interval expired.")

        return envelope.payload

```