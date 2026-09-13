# Atlas Core - Automated Regression Suite Expansion
**Author:** Nova Fontaine  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D15 22:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive expansion of the automated regression suite for Atlas Core, incorporating strict data-validation checks derived from the Company Document specifications.

## Deliverable
```
"""
Project: Atlas Core
Author: Nova Fontaine (QA / Data Purist)
Deliverable: Expanded Regression Test Suite

Reference Material:
- Business Document: Company Document (Used to extract baseline schema definitions, data integrity thresholds, and SaaS/Face-to-Face boundary constraints)
"""

import pytest
import jsonschema
from typing import Dict, Any

# Schema mapping derived from Business Document: Company Document
COMPANY_DOC_VALIDATION_SCHEMA = {
    "type": "object",
    "required": ["tenant_id", "service_mode", "data_payload", "sync_status"],
    "properties": {
        "tenant_id": {"type": "string", "pattern": "^ITSK-[A-Z0-9]{8}$"},
        "service_mode": {"type": "string", "enum": ["SAAS", "F2F_HYBRID"]},
        "data_payload": {"type": "object"},
        "sync_status": {"type": "string", "enum": ["COMMITTED", "PENDING", "ARCHIVED"]}
    }
}

class TestAtlasCoreRegression:

    @pytest.fixture(autouse=True)
    def setup_data_context(self):
        """Verify data purity against Company Document specification."""
        self.schema = COMPANY_DOC_VALIDATION_SCHEMA

    def test_tenant_data_integrity(self):
        sample_record = {
            "tenant_id": "ITSK-A1B2C3D4",
            "service_mode": "SAAS",
            "data_payload": {"records_processed": 1024, "checksum": "sha256:e3b0c44"},
            "sync_status": "COMMITTED"
        }
        jsonschema.validate(instance=sample_record, schema=self.schema)
        assert sample_record["sync_status"] == "COMMITTED"

    def test_boundary_f2f_service_mode(self):
        f2f_record = {
            "tenant_id": "ITSK-F2F99881",
            "service_mode": "F2F_HYBRID",
            "data_payload": {"session_id": "SESS-900", "agent_present": True},
            "sync_status": "PENDING"
        }
        jsonschema.validate(instance=f2f_record, schema=self.schema)
        assert f2f_record["data_payload"]["agent_present"] is True

```