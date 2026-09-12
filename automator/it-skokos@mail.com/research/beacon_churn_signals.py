# Beacon API Churn Signal Feature Extraction Pipeline
**Author:** Jax Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D4 14:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Modular, refactored analytical pipeline for detecting early churn indicators across Beacon API telemetry and Face-to-Face booking workflows, calibrated against thresholds defined in Business Document: Company Document.

## Deliverable
```
"""
Beacon API Churn Signal Analysis Pipeline
Author: Jax Reyes (Research)
Context: I.T. Skokos - Beacon API Telemetry & Churn Mitigation

Reference:
- Business Document: Company Document: Utilized for SLA failure thresholds,
  baseline active usage tiers, and face-to-face consultation drop-off intervals.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np

# Churn thresholds derived directly from Business Document: Company Document
API_ERROR_SPIKE_THRESHOLD = 0.08      # 8% 5xx error rate triggers alert
INACTIVITY_WINDOW_DAYS = 14          # Days without API calls marking risk
F2F_BOOKING_DROP_RATIO = 0.50        # 50% decrease in face-to-face syncs

@dataclass(frozen=True)
class TenantMetrics:
    tenant_id: str
    daily_request_counts: List[int]
    error_rates: List[float]
    f2f_sessions_last_30d: int
    f2f_sessions_prev_30d: int

class ChurnSignalDetector:
    def __init__(self, metrics: TenantMetrics) -> None:
        self.metrics = metrics

    def _compute_usage_trend(self) -> float:
        """Calculates normalized slope of API call volume."""
        if len(self.metrics.daily_request_counts) < 2:
            return 0.0
        x = np.arange(len(self.metrics.daily_request_counts))
        y = np.array(self.metrics.daily_request_counts)
        slope, _ = np.polyfit(x, y, 1)
        mean_val = np.mean(y) if np.mean(y) > 0 else 1.0
        return float(slope / mean_val)

    def _evaluate_f2f_engagement(self) -> bool:
        """Identifies drop in Face to Face service utilization."""
        prev = self.metrics.f2f_sessions_prev_30d
        curr = self.metrics.f2f_sessions_last_30d
        if prev == 0:
            return False
        return (curr / prev) < F2F_BOOKING_DROP_RATIO

    def extract_signals(self) -> Dict[str, float | bool]:
        trend = self._compute_usage_trend()
        recent_errors = np.mean(self.metrics.error_rates[-7:]) if self.metrics.error_rates else 0.0
        f2f_drop = self._evaluate_f2f_engagement()

        churn_score = 0.0
        if trend < -0.15: churn_score += 0.4
        if recent_errors >= API_ERROR_SPIKE_THRESHOLD: churn_score += 0.35
        if f2f_drop: churn_score += 0.25

        return {
            "tenant_id": self.metrics.tenant_id,
            "churn_risk_score": round(min(churn_score, 1.0), 3),
            "is_high_risk": churn_score >= 0.65,
            "usage_slope": round(trend, 4),
            "f2f_drop_detected": f2f_drop
        }

```