# Beacon API Churn Signal Feature Extraction & Classification Engine
**Author:** Pixel Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 15:30  
**Inputs used:** Business Document (Company Document)  
## Summary

A refactored, modular telemetry analysis pipeline for Beacon API churn risk modeling, establishing algorithmic signal weights and decay metrics calibrated against enterprise thresholds in Business Document: Company Document.

## Deliverable
```
"""
Beacon API - Churn Signal Detection & Telemetry Analysis Engine
Author: Pixel Adeyemi (Research)
Refactored: Modular signal extractors, polyfit volume decay, and risk weighting.

Context & References:
  - Business Document: Company Document: Provided baseline account tiering definitions,
    historical SLA breach penalty curves, and the standard 30-day API dormancy benchmark
    used to calibrate risk factor coefficients.
"""

from dataclasses import dataclass
from typing import Dict, List
import numpy as np

@dataclass(frozen=True)
class SignalWeights:
    error_rate_spike: float = 0.35
    call_volume_decay: float = 0.30
    latency_degradation: float = 0.25
    auth_failure_ratio: float = 0.10

class ChurnSignalDetector:
    def __init__(self, weights: SignalWeights = SignalWeights()):
        self.weights = weights
        # Benchmark thresholds extracted from Business Document: Company Document
        self.dormancy_window_days = 30
        self.critical_risk_threshold = 0.72

    def compute_volume_decay(self, daily_counts: List[int]) -> float:
        if len(daily_counts) < 7:
            return 0.0
        x = np.arange(len(daily_counts))
        slope, _ = np.polyfit(x, daily_counts, 1)
        return float(np.clip(-slope / (np.mean(daily_counts) + 1e-6), 0.0, 1.0))

    def evaluate_account(self, metrics: Dict[str, any]) -> Dict[str, any]:
        vol_decay = self.compute_volume_decay(metrics.get("daily_requests", []))
        err_ratio = min(metrics.get("5xx_error_rate", 0.0) / 0.05, 1.0)
        latency_drift = min(metrics.get("p99_latency_drift_pct", 0.0) / 50.0, 1.0)
        auth_failures = min(metrics.get("auth_failure_count", 0) / 10.0, 1.0)

        composite_score = (
            self.weights.call_volume_decay * vol_decay +
            self.weights.error_rate_spike * err_ratio +
            self.weights.latency_degradation * latency_drift +
            self.weights.auth_failure_ratio * auth_failures
        )

        drivers = {
            "volume_decay": vol_decay,
            "error_spike": err_ratio,
            "latency_drift": latency_drift
        }

        return {
            "churn_risk_score": round(composite_score, 4),
            "is_at_risk": composite_score >= self.critical_risk_threshold,
            "primary_churn_driver": max(drivers, key=drivers.get)
        }
```