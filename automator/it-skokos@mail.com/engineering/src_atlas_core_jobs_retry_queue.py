# Atlas Core: Secure Retry Queue and Job Runner Implementation
**Author:** Rune Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 20:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a fault-tolerant, security-hardened retry queue for Atlas Core featuring exponential backoff, payload HMAC validation, and quarantine dead-letter queue (DLQ) integration governed by Company Document.

## Deliverable
```
"""
Atlas Core - Secure Job Retry Runner
Author: Rune Okafor (Engineering)
Reference: Adheres strictly to security and fault-tolerance baselines in 'Company Document'.
"""

import hmac
import hashlib
import json
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("atlas_core.retry_runner")

class SecureRetryQueueRunner:
    def __init__(self, secret_key: bytes, max_retries: int = 5, base_delay: float = 2.0):
        # Enforce conservative retry thresholds as mandated by Company Document section 4.2
        self.secret_key = secret_key
        self.max_retries = min(max_retries, 5)
        self.base_delay = base_delay
        self.dlq: list[Dict[str, Any]] = []

    def _verify_payload_integrity(self, job: Dict[str, Any]) -> bool:
        expected_sig = job.get("signature")
        payload_raw = json.dumps(job.get("payload", {}), sort_keys=True).encode()
        calculated = hmac.new(self.secret_key, payload_raw, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig or "", calculated)

    def enqueue_retry(self, job: Dict[str, Any], error: Exception) -> bool:
        if not self._verify_payload_integrity(job):
            logger.critical(f"[SECURITY] Integrity verification failed for job {job.get('id')}. Quarantining immediately.")
            self._quarantine(job, "INTEGRITY_COMPROMISED")
            return False

        attempts = job.get("retry_count", 0) + 1
        if attempts > self.max_retries:
            logger.warning(f"Job {job.get('id')} exceeded max retries ({self.max_retries}). Moving to DLQ.")
            self._quarantine(job, f"MAX_RETRIES_EXCEEDED: {str(error)}")
            return False

        job["retry_count"] = attempts
        backoff = self.base_delay * (2 ** (attempts - 1))
        job["next_run_epoch"] = time.time() + backoff
        logger.info(f"Job {job.get('id')} scheduled for retry #{attempts} in {backoff}s.")
        return True

    def _quarantine(self, job: Dict[str, Any], reason: str) -> None:
        # Secure DLQ isolation conforming to Company Document incident response specs
        quarantined_record = {
            "job": job,
            "quarantine_reason": reason,
            "quarantined_at": time.time()
        }
        self.dlq.append(quarantined_record)

```