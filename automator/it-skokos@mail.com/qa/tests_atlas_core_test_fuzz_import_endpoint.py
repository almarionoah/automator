# Atlas Core - Import Endpoint Lightweight Fuzz Testing Harness
**Author:** Onyx Hale  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D12 17:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Lean automated fuzz testing suite for the Atlas Core /api/v1/import endpoint, utilizing lightweight local payload mutations based on thresholds defined in Company Document to minimize cloud compute and third-party SaaS testing costs.

## Deliverable
```
# Project: Atlas Core
# QA Engineer: Onyx Hale (Cost-Cutter Style)
# Description: Low-overhead mutation fuzzing harness for /api/v1/import
# Context: Governed by specifications in 'Business Document: Company Document'

import os
import random
import string
import json
import pytest
import requests

BASE_URL = os.getenv("ATLAS_CORE_URL", "http://localhost:8080")
IMPORT_ENDPOINT = f"{BASE_URL}/api/v1/import"

# Reference: 'Company Document' was utilized to extract expected schema fields,
# tier-1 error code boundaries (400 vs 500), and rate-limit guardrails to
# avoid incurring unnecessary autoscaling cloud compute costs during testing.

SEEDS = [
    {"customer_id": 101, "service_type": "SaaS", "records": [{"id": 1, "status": "active"}]},
    {"customer_id": 202, "service_type": "F2F", "records": [{"id": 2, "location": "Site-A"}]},
]

def mutate_payload(base_payload):
    mutation_type = random.choice(["overflow", "type_swap", "null_inject", "unicode", "truncation"])
    data = json.loads(json.dumps(base_payload))
    if mutation_type == "overflow":
        data["records"] = [{"overflow": "A" * 50000}]
    elif mutation_type == "type_swap":
        data["customer_id"] = "INVALID_STRING_ID"
    elif mutation_type == "null_inject":
        data["service_type"] = "\x00\x00\x00"
    elif mutation_type == "unicode":
        data["records"] = [{"meta": "\u202e\u0000\uffff"}]
    elif mutation_type == "truncation":
        return json.dumps(data)[: len(json.dumps(data)) // 2]
    return json.dumps(data)

@pytest.mark.parametrize("iteration", range(50))
def test_fuzz_import_endpoint(iteration):
    seed = random.choice(SEEDS)
    payload = mutate_payload(seed)
    headers = {"Content-Type": "application/json", "X-Cost-Optimized-Test": "true"}

    response = requests.post(IMPORT_ENDPOINT, data=payload, headers=headers, timeout=3.0)

    # Company Document stipulates 500-series unhandled crashes are critical defects;
    # 400-422 status codes represent acceptable input sanitization.
    assert response.status_code != 500, f"Fuzz crash detected on iteration {iteration}: {response.text}"
    assert response.status_code in [200, 202, 400, 413, 422], f"Unexpected code {response.status_code}"

```