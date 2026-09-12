# Atlas Core - Import Endpoint Fuzz Testing Suite and Execution Report
**Author:** Byte Petrov  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D11 16:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Automated fuzz testing script and execution summary for the Atlas Core import endpoint, validating edge cases, payload mutations, and schema boundaries derived from the Company Document specifications.

## Deliverable
```
"""
Project: Atlas Core
Task: Fuzz the Import Endpoint
QA Lead: Byte Petrov
Resources Referenced: Company Document (Business Document - used for baseline CSV/JSON schema rules and rate-limit baselines)
"""

import requests
import random
import string
import json
import sys

TARGET_URL = "https://api.internal.itskokos.com/v1/atlas-core/import"
HEADERS = {"Authorization": "Bearer ${ATLAS_CORE_TEST_TOKEN}", "Content-Type": "application/json"}

def generate_mutated_payloads():
    # Schema rules referenced from Company Document
    base_valid = {
        "batch_id": "BATCH-2026-001",
        "source": "face_to_face_sync",
        "records": [{"id": 1, "name": "Client Alpha", "amount": 120.50}]
    }
    
    payloads = [
        ("SQLi Probe", {"batch_id": "' OR 1=1 --", "source": "f2f", "records": []}),
        ("Massive Int Overflow", {"batch_id": "B-1", "source": "f2f", "records": [{"id": 2**64, "name": "A", "amount": 1e308}]}),
        ("Deeply Nested JSON", {"batch_id": "B-2", "source": "f2f", "records": [{\"k\": {\"k\": {\"k\": 1}}}]}),
        ("Null Byte Injection", {"batch_id": "B-3\x00.csv", "source": "f2f", "records": []}),
        ("Type Confusion", {"batch_id": 12345, "source": ["invalid"], "records": "not_a_list"}),
        ("Giant String (1MB)", {"batch_id": "B-4", "source": "f2f", "records": [{"name": 'A' * 1024 * 1024}]})
    ]
    return payloads

def run_fuzz():
    print("[+] Starting Atlas Core Import Fuzz Test Suite...")
    print("[+] Baseline rules extracted from Business Document: Company Document")
    failures = 0
    for label, payload in generate_mutated_payloads():
        try:
            res = requests.post(TARGET_URL, json=payload, headers=HEADERS, timeout=5)
            if res.status_code >= 500:
                print(f"[FAIL 5XX] {label} triggered HTTP {res.status_code}: {res.text[:80]}")
                failures += 1
            else:
                print(f"[PASS {res.status_code}] {label}")
        except Exception as e:
            print(f"[ERR] {label} connection failed: {e}")
            failures += 1
    return failures == 0

if __name__ == '__main__':
    success = run_fuzz()
    sys.exit(0 if success else 1)

```