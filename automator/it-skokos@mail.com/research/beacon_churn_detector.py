# Beacon API Churn Signal Detection Framework
**Author:** Iris Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D13 05:40  
**Inputs used:** Business Document (Company Document)  
## Summary

A refactored churn signal detection module and telemetry spec for the Beacon API project, analyzing event telemetry against the baselines established in Company Document.

## Deliverable
```
"""
Beacon API - Churn Signal Detection Service
Author: Iris Okafor (Research)
Context: Derived from baseline churn criteria in Business Document: Company Document.
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import numpy as np

@dataclass(frozen=True)
class TelemetrySnapshot:
    tenant_id: str
    api_call_volume_7d: int
    api_call_volume_30d: int
    error_rate_4xx: float
    error_rate_5xx: float
    f2f_service_sessions_30d: int
    days_since_last_active: int

class ChurnSignalEvaluator:
    """
    Evaluates tenant risk scores by comparing observed telemetry against
    thresholds mapped from 'Company Document' (Business Document).
    """

    def __init__(self, weights: Dict[str, float] = None):
        # Baseline weights aligned with retention drivers in Company Document
        self.weights = weights or {
            "usage_drop": 0.40,
            "error_frequency": 0.25,
            "f2f_engagement_gap": 0.20,
            "inactivity": 0.15
        }

    def compute_risk_score(self, snapshot: TelemetrySnapshot) -> Dict[str, Any]:
        # Usage velocity: 7-day average vs 30-day baseline
        expected_7d = snapshot.api_call_volume_30d / 4.0
        usage_drop_ratio = 1.0 - (snapshot.api_call_volume_7d / expected_7d) if expected_7d > 0 else 1.0
        usage_score = float(np.clip(usage_drop_ratio, 0.0, 1.0))

        # Error degradation factor
        error_score = float(np.clip((snapshot.error_rate_4xx + snapshot.error_rate_5xx) / 0.10, 0.0, 1.0))

        # Face-to-Face service engagement metric per Company Document recommendations
        f2f_score = 1.0 if snapshot.f2f_service_sessions_30d == 0 else 0.0

        # Inactivity factor (threshold = 14 days)
        inactivity_score = float(np.clip(snapshot.days_since_last_active / 14.0, 0.0, 1.0))

        composite_score = (
            self.weights["usage_drop"] * usage_score +
            self.weights["error_frequency"] * error_score +
            self.weights["f2f_engagement_gap"] * f2f_score +
            self.weights["inactivity"] * inactivity_score
        )

        return {
            "tenant_id": snapshot.tenant_id,
            "composite_churn_risk": round(composite_score, 4),
            "risk_tier": "HIGH" if composite_score >= 0.65 else "MEDIUM" if composite_score >= 0.35 else "LOW",
            "components": {
                "usage_drop_score": round(usage_score, 3),
                "error_score": round(error_score, 3),
                "f2f_gap_score": round(f2f_score, 3),
                "inactivity_score": round(inactivity_score, 3)
            }
        }

```