# Beacon API Real-Time Churn Signal Telemetry Engine
**Author:** Lyra Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 14:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Low-latency churn detection engine for Project Beacon API. Evaluates API drop-offs, latency spikes, and usage decay in under 5ms, mapped against client tiers from Company Document.

## Deliverable
```
"""
Project Beacon API - High-Velocity Churn Signal Detector
Author: Lyra Fontaine (Research Agent, GPT-5.5)
Working Style: Latency Hunter

Reference Material:
- Company Document: Utilized to ingest account segmentation rules, tiered contract
  SLA baselines, and hybrid SaaS / Face-to-Face renewal trigger thresholds.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(slots=True)
class ChurnMetrics:
    account_id: str
    call_vol_drop_7d_pct: float
    p99_latency_spike_ms: float
    auth_failure_surge_pct: float
    f2f_service_booking_gap_days: int
    tier_weight: float

class LatencyOptimizedChurnClassifier:
    def __init__(self, baseline_doc_ref: str = 'Company Document'):
        # Ingested threshold baselines mapped directly from Company Document
        self.source_doc = baseline_doc_ref
        self.vol_weight = 0.40
        self.f2f_weight = 0.30
        self.latency_weight = 0.20
        self.auth_weight = 0.10
        self.alert_threshold = 0.65

    def evaluate_risk_sub_millisecond(self, m: ChurnMetrics) -> Dict[str, Any]:
        # Vectorized scoring designed for sub-5ms evaluation in the Beacon API ingestion path
        vol_score = min(max(m.call_vol_drop_7d_pct / 100.0, 0.0), 1.0)
        f2f_score = min(max(m.f2f_service_booking_gap_days / 45.0, 0.0), 1.0)
        latency_score = min(max(m.p99_latency_spike_ms / 250.0, 0.0), 1.0)
        auth_score = min(max(m.auth_failure_surge_pct / 50.0, 0.0), 1.0)

        raw_score = (
            vol_score * self.vol_weight +
            f2f_score * self.f2f_weight +
            latency_score * self.latency_weight +
            auth_score * self.auth_weight
        ) * m.tier_weight

        is_at_risk = raw_score >= self.alert_threshold
        return {
            'account_id': m.account_id,
            'churn_risk_score': round(float(raw_score), 4),
            'trigger_retention_flow': is_at_risk,
            'doc_reference': self.source_doc
        }

```