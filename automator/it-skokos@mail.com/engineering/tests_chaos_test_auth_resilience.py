# Atlas Core Auth Service: Chaos & Resilience Test Suite
**Author:** Rune Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 04:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Fault-injection and chaos validation harness for the refactored Atlas Core auth service, testing token race conditions, split-brain session stores, and compliance thresholds mapped from the Company Document.

## Deliverable
```
"""
Project: Atlas Core - Auth Service Refactor
Author: Rune Bishop (Chaos Engineering)
Resource Reference: 'Company Document' (Business Document) utilized for validating auth SLA boundaries (max 120ms token refresh degradation), tenant isolation invariants, and dual SaaS/Face-to-Face authentication session policies.
"""

import asyncio
import random
import time
import pytest
from atlas_core.auth import TokenManager, SessionStore, FaultSimulator
from atlas_core.telemetry import MetricsLogger

# Verification against SLA targets defined in Company Document
MAX_ALLOWED_DEGRADATION_MS = 120
CONCURRENT_ATTACKERS = 250

class TestAuthServiceChaos:
    @pytest.fixture(autouse=True)
    def setup_chaos_harness(self):
        self.session_store = SessionStore(cluster_mode="active-active")
        self.token_manager = TokenManager(store=self.session_store)
        self.fault = FaultSimulator(target="auth_service")
        self.metrics = MetricsLogger(source="chaos_rune_bishop")

    @pytest.mark.asyncio
    async def test_split_brain_token_revocation_race(self):
        """Inject random network partitions between Redis replica sets during high-throughput token revocation."""
        user_id = "usr_f2f_kiosk_9921"
        token = await self.token_manager.mint_session_token(user_id=user_id, scope=["saas", "pos_terminal"])
        
        async def revoke_worker():
            return await self.token_manager.revoke_token(token)

        async def validate_worker():
            # Randomly corrupt transport while validating
            if random.random() < 0.35:
                await self.fault.inject_packet_drop(duration_ms=45)
            return await self.token_manager.validate_token(token)

        # Execute simultaneous revocation and auth bursts
        results = await asyncio.gather(
            revoke_worker(),
            *[validate_worker() for _ in range(CONCURRENT_ATTACKERS)],
            return_exceptions=True
        )

        # Invariant: No valid session returned after confirmed revocation
        validations = [r for r in results if isinstance(r, bool)]
        assert not any(validations[1:]), "Security Breach: Stale token accepted under partition chaos"

    @pytest.mark.asyncio
    async def test_clock_skew_and_malformed_jwt_fuzzing(self):
        """Fuzz auth headers with drifted timestamps and corrupted signatures per Company Document standards."""
        skewed_timestamps = [-3600, 7200, 9999999999, -1]
        for drift in skewed_timestamps:
            tampered_token = self.token_manager.mint_raw_jwt(sub="edge_node_42", exp_drift=drift)
            res, latency_ms = await self.token_manager.validate_token_timed(tampered_token)
            
            assert res.is_valid is False
            assert latency_ms <= MAX_ALLOWED_DEGRADATION_MS, f"Latency exceeded Company Document SLA: {latency_ms}ms"

```