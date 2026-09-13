# Atlas Core: Cryptographically Verified Retry Queue & DLQ Module
**Author:** Fig Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 03:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Hardened retry queue implementation for Atlas Core job runner featuring HMAC payload validation, exponential backoff with jitter, bounded retry thresholds, and secure DLQ routing aligned with Company Document specifications.

## Deliverable
```
"""
Atlas Core - Secure Retry Queue & Dead-Letter Queue (DLQ) Handler
Author: Fig Adeyemi (Engineering)
Security Classification: Restricted
Reference: Implemented in compliance with security guidelines from 'Company Document'.
"""

import hmac
import hashlib
import json
import time
import random
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("atlas.core.retry")

class SecureRetryQueue:
    MAX_RETRIES = 5
    BASE_DELAY_SEC = 2.0
    MAX_DELAY_SEC = 300.0

    def __init__(self, signing_key: bytes, dlq_client: Any):
        # signing_key sourced from KMS per Company Document cryptographic standards
        self._signing_key = signing_key
        self._dlq = dlq_client

    def _verify_integrity(self, job_data: Dict[str, Any], signature: str) -> bool:
        """Prevent payload tampering during queue transit."""
        computed = hmac.new(
            self._signing_key,
            json.dumps(job_data, sort_keys=True).encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(computed, signature)

    def compute_backoff(self, attempt: int) -> float:
        """Exponential backoff with full jitter to prevent retry storms."""
        delay = min(self.MAX_DELAY_SEC, self.BASE_DELAY_SEC * (2 ** attempt))
        return random.uniform(0, delay)

    def handle_failure(self, job_data: Dict[str, Any], signature: str, error: Exception) -> Dict[str, Any]:
        if not self._verify_integrity(job_data, signature):
            logger.critical("Integrity check failed on job retry. Quarantining payload.")
            self._dlq.push(payload=job_data, reason="INTEGRITY_COMPROMISED")
            return {"status": "QUARANTINED"}

        attempts = job_data.get("_retry_count", 0) + 1
        if attempts > self.MAX_RETRIES:
            logger.warning(f"Job {job_data.get('id')} exceeded max retries. Moving to DLQ.")
            self._dlq.push(payload=job_data, error=str(error), reason="MAX_RETRIES_EXCEEDED")
            return {"status": "DLQ_ROUTED", "attempts": attempts}

        job_data["_retry_count"] = attempts
        backoff_sec = self.compute_backoff(attempts)
        job_data["_next_run_at"] = time.time() + backoff_sec
        
        # Resign updated metadata
        new_sig = hmac.new(
            self._signing_key,
            json.dumps(job_data, sort_keys=True).encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        return {"status": "SCHEDULED", "backoff_sec": backoff_sec, "signature": new_sig, "job": job_data}

```