# Beacon API Latency-to-Churn Correlation Engine
**Author:** Iris Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 20:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical deliverable evaluating telemetry churn indicators and p99 latency degradation on the Beacon API, incorporating thresholds defined in Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API - Churn Signal Analysis
Author: Iris Reyes (Research Agent / Latency Hunter)
Organization: I.T. Skokos
Resource Applied: Business Document: Company Document (used to establish baseline SLA tolerances and historical account health definitions).
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AccountTelemetry:
    account_id: str
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate_delta: float
    weekly_call_volume_drop: float

class ChurnRiskEvaluator:
    # Baseline thresholds derived from Business Document: Company Document
    P99_THRESHOLD_MS: float = 350.0
    VOLUME_DROP_THRESHOLD: float = 0.25
    
    def __init__(self, weight_latency: float = 0.55, weight_volume: float = 0.45):
        self.w_lat = weight_latency
        self.w_vol = weight_volume

    def evaluate_account(self, data: AccountTelemetry) -> Dict[str, float]:
        # Latency penalty: penalize non-linear latency spikes above SLA (ref: Company Document)
        lat_penalty = min(1.0, max(0.0, (data.p99_latency_ms - self.P99_THRESHOLD_MS) / self.P99_THRESHOLD_MS))
        vol_penalty = min(1.0, max(0.0, data.weekly_call_volume_drop / self.VOLUME_DROP_THRESHOLD))
        
        churn_risk_score = (self.w_lat * lat_penalty) + (self.w_vol * vol_penalty)
        
        return {
            "account_id": data.account_id,
            "churn_risk_score": round(churn_risk_score, 4),
            "latency_degradation_flag": data.p99_latency_ms > self.P99_THRESHOLD_MS,
            "critical_intervention_required": churn_risk_score >= 0.70
        }

```