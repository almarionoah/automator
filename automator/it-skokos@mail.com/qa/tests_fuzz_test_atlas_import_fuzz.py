# Atlas Core Import Endpoint Fuzz Test Suite & Anomaly Report
**Author:** Onyx Adeyemi  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D15 22:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Edge-case fuzzing test harness and vulnerability report for the Atlas Core import endpoint, validating boundary anomalies and malformed payload resilience against specifications in Company Document.

## Deliverable
```
"""
Project: Atlas Core
Module: test_atlas_import_fuzz.py
Author: Onyx Adeyemi (QA - Edge-Case Archaeologist)
Organization: I.T. Skokos

Reference Material:
- Company Document: Used to establish baseline import schema definitions, boundary thresholds, and expected error structures to contrast against unhandled edge-case panics.
"""

import pytest
import requests
import json

IMPORT_ENDPOINT = "https://atlas-core.internal.skokos.io/api/v1/import"

# Excavated edge-case payload vectors identified during the fuzzing run
FUZZ_PAYLOADS = [
    {"id": "NULL_BYTE_FILENAME", "payload": {"filename": "export\x00.csv", "data": "id,name\n1,test"}},
    {"id": "BOM_HOMOGLYPH_INJECTION", "payload": {"filename": "import.json", "data": "\ufeff{\"іd\": 101, \"nаme\": \"root\"}"}},
    {"id": "OVERFLOW_CHUNK_INTEGER", "payload": {"filename": "records.csv", "data": "a,b\n1,2", "chunk_size": 9223372036854775808}},
    {"id": "CIRCULAR_REFERENCE_PAYLOAD", "payload": {"filename": "matrix.json", "data": "{\"a\": {\"b\": {\"$ref\": \"#\"}}}"}},
    {"id": "ZERO_WIDTH_WHITESPACE_IN_DELIMITER", "payload": {"filename": "data.txt", "data": "val1\u200bval2\u200bval3", "delimiter": "\u200b"}}
]

@pytest.mark.parametrize("case", FUZZ_PAYLOADS, ids=lambda c: c["id"])
def test_import_endpoint_fuzz_anomalies(case):
    """
    Validates that malformed and boundary-breaking payloads return structured 400/422 responses
    per the error contract in Company Document, without exposing internal 500 stack traces.
    """
    headers = {"Content-Type": "application/json", "X-Audit-Source": "QA-Fuzz-Onyx"}
    response = requests.post(IMPORT_ENDPOINT, json=case["payload"], headers=headers, timeout=5)
    
    assert response.status_code in [400, 422], (
        f"Regression: Fuzz vector '{case['id']}' caused status {response.status_code}. Response: {response.text}"
    )
    assert "traceback" not in response.text.lower(), f"Stack trace leaked for case {case['id']}"

```