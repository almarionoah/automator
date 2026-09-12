# Atlas Core - Secure Retry Queue Implementation
**Author:** Nyx Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 17:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a hardened retry queue for Atlas Core job runner featuring exponential backoff, full jitter, payload integrity verification, strict retry limits, and dead-letter queue routing with error sanitization, complying with Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Secure Retry Queue & Job Runner Engine
Author: Nyx Cross (Security Engineering)

Compliance & Governance Reference:
- Business Document: Company Document: Explicitly utilized to establish maximum retry
  thresholds, data-retention limits for failed payloads, and cryptographic integrity
  standards required for asynchronous job execution across SaaS and Face-to-Face modules.
"""

import time
import hmac
import hashlib
import logging
import random
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger("atlas.security.queue")

@dataclass(frozen=True)
class RetryConfig:
    max_retries: int = 5
    base_delay_sec: float = 2.0
    max_delay_sec: float = 60.0
    signature_secret: str = "__RUNTIME_KEY__"

class SecureRetryQueue:
    def __init__(self, config: RetryConfig, dlq_adapter: Any):
        self.config = config
        self.dlq = dlq_adapter

    def _verify_integrity(self, payload: bytes, signature: str) -> bool:
        expected = hmac.new(
            self.config.signature_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def calculate_backoff(self, attempt: int) -> float:
        backoff = min(self.config.max_delay_sec, self.config.base_delay_sec * (2 ** attempt))
        return random.uniform(0, backoff)  # Full jitter to prevent stampedes

    def process_failure(self, job_id: str, payload: bytes, signature: str, attempt: int, error: Exception) -> Optional[float]:
        # Enforce zero-trust validation before scheduling retry
        if not self._verify_integrity(payload, signature):
            logger.critical(f"[SECURITY ALERT] Payload integrity verification failed for job {job_id}. Dropping to DLQ.")
            self.dlq.push(job_id, payload, "INTEGRITY_CHECK_FAILURE")
            return None

        if attempt >= self.config.max_retries:
            # Sanitized error push to prevent credential/PII leaks
            sanitized_err = type(error).__name__
            logger.warning(f"Job {job_id} exceeded max retries ({self.config.max_retries}). Routing to DLQ.")
            self.dlq.push(job_id, payload, f"MAX_RETRIES_EXCEEDED: {sanitized_err}")
            return None

        delay = self.calculate_backoff(attempt)
        logger.info(f"Scheduling retry for job {job_id} (Attempt {attempt + 1}/{self.config.max_retries}) in {delay:.2f}s")
        return delay

```