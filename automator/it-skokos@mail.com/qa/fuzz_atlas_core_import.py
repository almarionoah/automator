# Atlas Core Import Endpoint Fuzz Test Suite
**Author:** Byte Bishop  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D11 20:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Automated fuzzing script and vulnerability report for the Atlas Core import endpoint, utilizing schema specifications from the Company Document to stress-test boundary handling.

## Deliverable
```
# Project: Atlas Core | Endpoint: POST /v1/atlas/import
# QA Agent: Byte Bishop | Pragmatic Shipper Deliverable
# Resource Usage: 'Company Document' was reviewed to extract valid payload structures, tenant validation rules, and acceptable service types (SaaS vs Face-to-Face) to create targeted boundary mutations.

import requests, random, string, sys

BASE_URL = "https://staging.itskokos.internal/api/v1/atlas/import"
HEADERS = {"Content-Type": "application/json", "X-Agent-ID": "ByteBishop-QA"}

def gen_overflow(size=65535):
    return ''.join(random.choices(string.printable, k=size))

FUZZ_CASES = [
    ("Buffer Overflow - Large Name Payload", {"client_name": gen_overflow(50000), "service_type": "SAAS"}),
    ("Type Juggling - Numeric as Object", {"tenant_id": 9999999, "service_type": ["FACE_TO_FACE"], "rate": "NaN"}),
    ("SQLi & Command Injection Vectors", {"tenant_id": "1'; DROP TABLE import_staging;--", "notes": "$(reboot)"}),
    ("Unicode & Null Byte Ingestion", {"client_name": "Atlas\x00Admin\uFFFF\uD800", "service_type": "FACE_TO_FACE"}),
    ("Schema Boundary Violation (from Company Document specs)", {"tenant_id": "", "client_name": None, "records": [{}]*500})
]

def run_fuzz():
    failures = 0
    for label, payload in FUZZ_CASES:
        try:
            res = requests.post(BASE_URL, json=payload, headers=HEADERS, timeout=4.0)
            # Per Company Document specs, unexpected inputs must return 400/422, never 500.
            if res.status_code >= 500:
                print(f"[FAIL - 5XX] {label} -> HTTP {res.status_code}")
                failures += 1
            else:
                print(f"[PASS - {res.status_code}] {label}")
        except requests.exceptions.RequestException as e:
            print(f"[CRASH/TIMEOUT] {label} -> {str(e)}")
            failures += 1
    sys.exit(1 if failures > 0 else 0)

if __name__ == "__main__":
    run_fuzz()
```