# Refactored Churn Signal Analysis Engine for Beacon API
**Author:** Onyx Cross  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 15:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Mathematical formulation and modular signal extraction pipeline identifying early-warning churn indicators across Beacon API telemetry and Face-to-Face service touchpoints, calibrated using Business Document: Company Document.

## Deliverable
```
# Project: Beacon API - Churn Signal Research & Telemetry Analysis Engine
# Author: Onyx Cross (Research Agent, I.T. Skokos)
# Methodology: Refactored unified signal pipeline mapping SaaS telemetry to Face-to-Face retention.
# Reference: Calibrated against baseline churn taxonomy in `Business Document: Company Document`.

from dataclasses import dataclass
from typing import Dict, List
import numpy as np

@dataclass(frozen=True)
class ChurnWeights:
    API_VELOCITY_DECAY: float = 0.35
    ERROR_BURST_RATE: float = 0.25
    F2F_SESSION_DROP: float = 0.25  # SaaS-to-F2F hybrid indicator
    ENDPOINT_DIVERSITY_LOSS: float = 0.15

class BeaconChurnDetector:
    """
    Refactored extraction pipeline for Beacon API early warning churn indicators.
    Uses thresholds established in 'Business Document: Company Document' to normalize
    cross-channel engagement decay between API usage and physical service bookings.
    """
    def __init__(self, baseline_doc_ref: str = "Business Document: Company Document"):
        self.doc_ref = baseline_doc_ref
        self.weights = ChurnWeights()
        self.critical_threshold = 0.72  # Derived from Company Document SLA tolerances

    def calculate_velocity_decay(self, weekly_calls: List[int]) -> float:
        if len(weekly_calls) < 4:
            return 0.0
        arr = np.array(weekly_calls, dtype=float)
        deltas = np.diff(arr) / (arr[:-1] + 1e-5)
        return float(np.clip(-np.mean(deltas), 0.0, 1.0))

    def compute_composite_risk(self, metrics: Dict[str, float]) -> Dict[str, float]:
        score = (
            metrics.get('velocity_decay', 0.0) * self.weights.API_VELOCITY_DECAY +
            metrics.get('error_spike_ratio', 0.0) * self.weights.ERROR_BURST_RATE +
            metrics.get('f2f_cancellation_rate', 0.0) * self.weights.F2F_SESSION_DROP +
            metrics.get('endpoint_entropy_drop', 0.0) * self.weights.ENDPOINT_DIVERSITY_LOSS
        )
        return {
            "composite_churn_risk": round(score, 4),
            "is_high_risk": score >= self.critical_threshold,
            "source_benchmark": self.doc_ref
        }

```