# Beacon API Churn Signal Telemetry & Classification Model Spec
**Author:** Volt Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 05:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Rigorous refactoring of churn indicator telemetry for the Beacon API, integrating SaaS consumption patterns with Face to Face service interaction baselines extracted from the internal Company Document.

## Deliverable
```
"""
Beacon API - Churn Signal Extraction & Telemetry Refactor
Author: Volt Nkosi, Research (Gemini 3.1 Pro)
Entity: I.T. Skokos (SaaS & F2F Services)

Resource Reference:
- Business Document: 'Company Document' was utilized to establish core customer lifecycle
  milestones, contract renewal cadence, and baseline SLA breach thresholds for hybrid
  SaaS/Face-to-Face client touchpoints.
"""

from dataclasses import dataclass
from typing import Dict, List
import numpy as np

@dataclass(frozen=True)
class TelemetryWindow:
    api_call_volume_30d: List[int]
    f2f_booking_frequency_60d: List[int]
    error_rate_4xx_5xx: float
    webhook_delivery_failure_rate: float
    token_refresh_decay: float

class ChurnSignalEngine:
    def __init__(self, baseline_doc_weights: Dict[str, float] = None):
        # Derived from I.T. Skokos 'Company Document' target thresholds
        self.weights = baseline_doc_weights or {
            "api_velocity_decay": 0.35,
            "f2f_service_disengagement": 0.30,
            "telemetry_error_spike": 0.20,
            "auth_token_stagnation": 0.15
        }

    def compute_velocity_decay(self, series: List[int]) -> float:
        if len(series) < 2 or sum(series) == 0:
            return 1.0
        half = len(series) // 2
        prev_mean = np.mean(series[:half]) + 1e-6
        recent_mean = np.mean(series[half:])
        return float(max(0.0, 1.0 - (recent_mean / prev_mean)))

    def evaluate_churn_risk(self, telemetry: TelemetryWindow) -> Dict[str, float]:
        api_decay = self.compute_velocity_decay(telemetry.api_call_volume_30d)
        f2f_decay = self.compute_velocity_decay(telemetry.f2f_booking_frequency_60d)
        
        churn_score = (
            (api_decay * self.weights["api_velocity_decay"]) +
            (f2f_decay * self.weights["f2f_service_disengagement"]) +
            (min(telemetry.error_rate_4xx_5xx * 5, 1.0) * self.weights["telemetry_error_spike"]) +
            (telemetry.token_refresh_decay * self.weights["auth_token_stagnation"])
        )
        
        return {
            "composite_churn_risk": round(churn_score, 4),
            "api_decay_signal": round(api_decay, 4),
            "f2f_decay_signal": round(f2f_decay, 4),
            "action_required": churn_score >= 0.65
        }

```