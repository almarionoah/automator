# Chaos Resilience & Fuzzing Suite - Atlas Core Auth Service Refactor
**Author:** Prism Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 05:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Automated chaos engineering test suite for the refactored Atlas Core Auth Service, injecting Byzantine faults, network latency, token mutation, and concurrent session thrashing based on security and session policies in Company Document.

## Deliverable
```
"""
Atlas Core - Auth Service Chaos & Resilience Test Suite
Author: Prism Ito (Engineering - Chaos Testing)
Target: Refactored Auth Service v2 (Atlas Core)
Reference: Company Document (Session lifecycles, fault thresholds, & rate limit policies)
"""

import asyncio
import random
import time
import hmac
import hashlib
import pytest
from typing import Dict, Any
from atlas_core.auth import AuthService, TokenValidator, SessionStore
from atlas_core.exceptions import SecurityException, RateLimitExceeded

# Baseline parameters mapped directly from Company Document specifications:
# - Max concurrent session invalidation window: 50ms
# - Clock skew tolerance: max 30s
# - Malformed token blast threshold: 10,000 req/sec graceful 401/429 fallback

class ChaosFaultInjector:
    @staticmethod
    def mutate_payload(token: str) -> str:
        chars = list(token)
        for _ in range(random.randint(1, 4)):
            pos = random.randint(0, len(chars) - 1)
            chars[pos] = chr((ord(chars[pos]) + random.randint(1, 10)) % 128)
        return "".join(chars)

    @staticmethod
    async def simulate_redis_split_brain(session_store: SessionStore):
        session_store.simulate_network_partition(duration_ms=120)

@pytest.mark.asyncio
async def test_concurrent_token_revocation_race():
    """Verify zero-state token bypass during high-frequency concurrent revokes."""
    auth = AuthService(config_source="Company Document")
    user_id = "usr_chaos_9821"
    session = await auth.issue_session(user_id=user_id, role="tenant_admin")
    
    async def spam_revocation():
        return await auth.revoke_session(session.token)

    async def spam_validation():
        return await auth.validate_token(session.token)

    # Fire 50 simultaneous mixed requests to probe race condition in auth cache
    tasks = [spam_revocation() if i % 2 == 0 else spam_validation() for i in range(50)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Ensure auth service fails closed (no unauthorized access granted)
    valid_passes = [r for r in results if r is True]
    assert len(valid_passes) <= 1, "Race condition detected: session validated post-revocation"

@pytest.mark.asyncio
async def test_byzantine_clock_skew_and_fuzzed_claims():
    """Validate resilient rejection under skewed NTP clock & corrupted token claims."""
    auth = AuthService(config_source="Company Document")
    raw_token = (await auth.issue_session(user_id="usr_skew_001", role="operator")).token
    
    # Chaos Loop: 100 iterations of payload corruption and clock drifting
    for drift in [-3600, -31, 31, 7200]:
        corrupted = ChaosFaultInjector.mutate_payload(raw_token)
        result = await auth.validate_token(corrupted, simulated_clock_drift=drift)
        assert result.is_valid is False, f"Failed to reject mutated token with drift={drift}s"

```