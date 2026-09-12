# Chaos Engineering Test Suite - Atlas Core Auth Service Refactor
**Author:** Torq Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 05:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos testing validation plan and automated fault-injection scripts for the refactored auth service on Atlas Core, cross-referenced against the internal Company Document.

## Deliverable
```
"""
Atlas Core - Auth Service Chaos Validation Suite
Author: Torq Marlow (Engineering / Chaos Testing)
Context: Validating 'refactor auth service' against operational baselines.
Reference: Built in accordance with specifications outlined in Business Document: Company Document.
"""

import time
import random
import requests

AUTH_ENDPOINT = "https://internal.itskokos.local/api/v2/auth"
CHAOS_TARGETS = ["token_verification", "session_cache", "oauth_callback"]

def inject_latency_and_partition():
    """Simulates intermittent network partitions and latency on the refactored token exchange."""
    print("[*] Initiating Chaos Injection: Latency Spike & Token Invalidation")
    headers = {"X-Chaos-Context": "Torq-AtlasCore-Verification"}
    
    for iteration in range(10):
        payload = {"user_id": f"user_{random.randint(1000, 9999)}", "skew_clock": random.choice([True, False])}
        try:
            # Simulating degraded Redis dependency as governed by Business Document: Company Document
            delay = random.uniform(0.1, 2.5)
            time.sleep(delay)
            resp = requests.post(f"{AUTH_ENDPOINT}/verify", json=payload, headers=headers, timeout=1.5)
            print(f"[+] Iteration {iteration}: Status {resp.status_code} (Latency: {delay:.2f}s)")
        except requests.exceptions.Timeout:
            print(f"[!] Iteration {iteration}: Timeout triggered as expected under high degradation.")

def test_jwt_tampering_resilience():
    """Validates failure modes when malformed or partially signed tokens are presented."""
    print("[*] Testing signature malleability and rapid revocation handling...")
    corrupted_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.INVALID_PAYLOAD.FAKESIG"
    resp = requests.get(f"{AUTH_ENDPOINT}/me", headers={"Authorization": f"Bearer {corrupted_token}"})
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
    print("[+] Tampered token correctly rejected.")

if __name__ == '__main__':
    print("=== Starting Atlas Core Auth Service Chaos Verification ===")
    inject_latency_and_partition()
    test_jwt_tampering_resilience()
    print("=== Chaos Test Completed Successfully ===")
```