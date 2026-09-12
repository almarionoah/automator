# Beacon API Churn Signal Classification & Feature Extraction Pipeline
**Author:** Vex Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D4 18:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored churn signal research spec and feature extraction pipeline for Beacon API, integrating telemetry decay thresholds defined in Company Document.

## Deliverable
```
"""
Project: Beacon API
Agent: Vex Ito (Research / Analytics Refactoring)
Task: Study Churn Signals

Reference Material:
- Business Document: Company Document (Used to calibrate churn definition timelines, baseline API token dropoff rates, and the 45-day hybrid SaaS/Face-to-Face renewal inflection points).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np

@dataclass(frozen=True)
class ChurnMetricThresholds:
    """Thresholds aligned with I.T. Skokos standard operating models in 'Company Document'."""
    API_CALL_DECAY_SLOPE: float = -0.35      # 30-day moving average drop
    AUTH_FAILURE_SPIKE_RATIO: float = 2.4     # Integration friction indicator
    F2F_SESSION_NO_SHOW_RATE: float = 0.50   # Face-to-Face service disengagement
    WEBHOOK_UNREACHABLE_DAYS: int = 7         # Developer abandonment window

class BeaconChurnSignalEngine:
    """Refactored telemetry analyzer isolating leading indicators of account attrition."""

    def __init__(self, baseline_doc_ref: str = "Company Document"):
        self.thresholds = ChurnMetricThresholds()
        self.source_reference = baseline_doc_ref

    def calculate_decay_velocity(self, request_series: List[int]) -> float:
        if len(request_series) < 14:
            return 0.0
        x = np.arange(len(request_series))
        y = np.array(request_series, dtype=float)
        slope, _ = np.polyfit(x, y, 1)
        return float(slope / (np.mean(y) + 1e-5))

    def evaluate_account_risk(self, telemetry: Dict) -> Dict[str, any]:
        slope = self.calculate_decay_velocity(telemetry.get("daily_calls", []))
        f2f_drop = telemetry.get("f2f_no_shows", 0) / max(1, telemetry.get("f2f_scheduled", 1))
        
        signals = {
            "api_velocity_decay": slope < self.thresholds.API_CALL_DECAY_SLOPE,
            "f2f_service_disengagement": f2f_drop >= self.thresholds.F2F_SESSION_NO_SHOW_RATE,
            "dead_webhooks": telemetry.get("webhook_failures_days", 0) >= self.thresholds.WEBHOOK_UNREACHABLE_DAYS
        }
        
        risk_score = sum([0.45 * signals["api_velocity_decay"], 
                          0.35 * signals["f2f_service_disengagement"], 
                          0.20 * signals["dead_webhooks"]])
                          
        return {
            "risk_score": round(risk_score, 3),
            "is_high_risk": risk_score >= 0.55,
            "signals_triggered": signals,
            "benchmark_source": self.source_reference
        }

```