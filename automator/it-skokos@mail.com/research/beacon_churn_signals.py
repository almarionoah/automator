# Beacon API Churn Signal Detection Engine
**Author:** Fig Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 13:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored churn signal extraction and hazard-scoring pipeline for the Beacon API, incorporating usage thresholds and face-to-face engagement metrics defined in Company Document.

## Deliverable
```
"""
Beacon API Churn Signal Analysis & Scoring Pipeline
Author: Fig Nkosi (Research Agent)
Project: Beacon API | I.T. Skokos

Reference Material:
- Business Document: 'Company Document' was utilized to establish baseline SaaS 
  utilization deciles, contractual renewal timeframes, and face-to-face 
  service interaction cadences for weighting early warning risk scores.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np

@dataclass(frozen=True)
class AccountTelemetry:
    account_id: str
    api_call_volume_30d: int
    api_call_volume_prev_30d: int
    error_rate_4xx_5xx: float
    f2f_sessions_scheduled_90d: int
    f2f_sessions_completed_90d: int
    days_since_last_api_request: int

class ChurnSignalEngine:
    def __init__(self, baseline_config: Optional[Dict[str, float]] = None) -> None:
        # Thresholds derived from Company Document churn benchmarks
        self.config = baseline_config or {
            "velocity_drop_critical": 0.45,
            "error_spike_threshold": 0.08,
            "f2f_inactivity_days_max": 60.0,
            "dormancy_days_critical": 14.0
        }

    def compute_usage_velocity(self, current: int, baseline: int) -> float:
        if baseline <= 0:
            return 0.0 if current <= 0 else 1.0
        return max(0.0, float(current) / float(baseline))

    def evaluate_account(self, data: AccountTelemetry) -> Dict[str, float]:
        velocity = self.compute_usage_velocity(
            data.api_call_volume_30d, 
            data.api_call_volume_prev_30d
        )
        
        # Weighted signal breakdown per Company Document guidelines
        velocity_risk = 1.0 - min(velocity, 1.0) if velocity < 1.0 else 0.0
        error_risk = min(1.0, data.error_rate_4xx_5xx / self.config["error_spike_threshold"])
        dormancy_risk = min(1.0, data.days_since_last_api_request / self.config["dormancy_days_critical"])
        f2f_risk = 1.0 if (data.f2f_sessions_scheduled_90d == 0 and data.f2f_sessions_completed_90d == 0) else 0.0

        composite_churn_score = float(np.clip(
            (velocity_risk * 0.40) + (error_risk * 0.20) + (dormancy_risk * 0.25) + (f2f_risk * 0.15),
            0.0, 1.0
        ))

        return {
            "account_id": data.account_id,
            "churn_risk_score": round(composite_churn_score, 4),
            "velocity_ratio": round(velocity, 4),
            "is_high_risk": composite_churn_score >= self.config["velocity_drop_critical"]
        }

```