# Beacon API: Refactored Churn Signal Telemetry & Risk Scoring Specification
**Author:** Ash Petrov  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 18:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Research specification and modular scoring engine evaluating churn signals for the Beacon API across SaaS telemetry and Face-to-Face service interactions, calibrated using baseline account criteria from the Company Document.

## Deliverable
```
"""
Beacon API Churn Signal Telemetry & Risk Scoring Engine
Author: Ash Petrov (Research, o3) | I.T. Skokos
Style: Iterative Refactor (v2.4 - Normalized Multi-Signal Aggregator)

Resource Reference:
- Business Document: 'Company Document' was utilized to extract baseline account tier
  definitions, standard SaaS-to-F2F engagement ratios, and contract renewal cycle
  thresholds to anchor signal sensitivity windows.
"""

from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum

class ChurnSeverity(str, Enum):
    LOW = "LOW"
    ELEVATED = "ELEVATED"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True)
class ChurnWeights:
    saas_api_decay: float = 0.35      # Beacon API call velocity drops (>40% 14d rolling)
    f2f_booking_drop: float = 0.30     # Face-to-face consultation cancellations (>25% WoW)
    auth_error_spike: float = 0.20     # Integration friction (4xx/5xx token validation anomalies)
    seat_dormancy: float = 0.15        # Inactive provisioned operator seats

class BeaconChurnEngine:
    def __init__(self, weights: ChurnWeights = ChurnWeights()):
        self.weights = weights
        total = sum([
            weights.saas_api_decay, weights.f2f_booking_drop,
            weights.auth_error_spike, weights.seat_dormancy
        ])
        assert round(total, 2) == 1.00, f"Signal weights must sum to 1.0 (got {total})"

    def evaluate_signals(self, tenant_telemetry: Dict[str, float]) -> Dict[str, Any]:
        # Normalize inputs [0.0 - 1.0]
        api_score = min(max(tenant_telemetry.get("api_velocity_decay_rate", 0.0), 0.0), 1.0)
        f2f_score = min(max(tenant_telemetry.get("f2f_cancellation_rate", 0.0), 0.0), 1.0)
        err_score = min(max(tenant_telemetry.get("auth_error_frequency_index", 0.0), 0.0), 1.0)
        seat_score = min(max(tenant_telemetry.get("dormant_seat_ratio", 0.0), 0.0), 1.0)

        composite = (
            (api_score * self.weights.saas_api_decay) +
            (f2f_score * self.weights.f2f_booking_drop) +
            (err_score * self.weights.auth_error_spike) +
            (seat_score * self.weights.seat_dormancy)
        )

        severity = ChurnSeverity.LOW
        if composite >= 0.65:
            severity = ChurnSeverity.CRITICAL
        elif composite >= 0.35:
            severity = ChurnSeverity.ELEVATED

        drivers = [
            ("saas_api_decay", api_score),
            ("f2f_booking_drop", f2f_score),
            ("auth_error_spike", err_score),
            ("seat_dormancy", seat_score)
        ]
        drivers.sort(key=lambda x: x[1], reverse=True)

        return {
            "risk_score": round(composite, 4),
            "severity": severity.value,
            "primary_churn_driver": drivers[0][0],
            "driver_breakdown": {k: round(v, 3) for k, v in drivers}
        }

```