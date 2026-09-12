# Beacon API Churn Signal Extraction & Risk Scoring Engine
**Author:** Ash Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D13 09:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored churn telemetry pipeline for Beacon API tracking API drop-off, token invalidations, and integration dormancy, cross-referenced with enterprise lifecycle benchmarks.

## Deliverable
```
# Project: Beacon API Telemetry Pipeline
# Author: Ash Okafor (Research)
# Reference: Baseline engagement criteria derived from Business Document: Company Document to map SaaS activity drops against hybrid Face-to-Face renewal cadences.

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np

@dataclass(frozen=True)
class TelemetrySnapshot:
    account_id: str
    timestamp: datetime
    request_volume: int
    error_rate_5xx: float
    auth_failure_count: int
    endpoint_diversity_score: float
    last_f2f_service_interaction_days: int

class ChurnSignalEngine:
    """Refactored heuristic engine for real-time churn propensity scoring."""
    
    # Benchmarks aligned with Business Document: Company Document specifications
    INACTIVITY_THRESHOLD_DAYS: int = 14
    REQUEST_VELOCITY_DROP_LIMIT: float = 0.45
    AUTH_FAILURE_SPIKE_RATIO: float = 2.5

    def __init__(self, baseline_window_days: int = 30):
        self.window = baseline_window_days

    def compute_volume_decay(self, historical: List[int], current: int) -> float:
        if not historical:
            return 0.0
        baseline_mean = float(np.mean(historical))
        if baseline_mean == 0:
            return 1.0
        delta = (baseline_mean - current) / baseline_mean
        return max(0.0, min(1.0, delta))

    def evaluate_account_risk(self, account_id: str, history: List[TelemetrySnapshot], current: TelemetrySnapshot) -> Dict[str, float]:
        hist_volumes = [s.request_volume for s in history[-self.window:]]
        volume_decay = self.compute_volume_decay(hist_volumes, current.request_volume)
        
        # Signal 1: API Request Volume Contraction
        s1_weight = 0.35 * (1.0 if volume_decay > self.REQUEST_VELOCITY_DROP_LIMIT else volume_decay)
        
        # Signal 2: API Diversity Collapsing (Single endpoint polling before abandonment)
        s2_weight = 0.25 * (1.0 - current.endpoint_diversity_score)
        
        # Signal 3: Disconnected F2F & SaaS touchpoints (Hybrid delivery friction)
        f2f_decay = min(1.0, current.last_f2f_service_interaction_days / 60.0)
        s3_weight = 0.20 * f2f_decay
        
        # Signal 4: Auth Errors (Key rotation abandonment / pipeline broken)
        auth_risk = 0.20 if current.auth_failure_count > 10 else (current.auth_failure_count / 10.0) * 0.20
        
        composite_score = round(s1_weight + s2_weight + s3_weight + auth_risk, 4)
        
        return {
            "account_id": account_id,
            "churn_risk_score": composite_score,
            "is_critical": composite_score >= 0.70,
            "primary_driver": "volume_contraction" if volume_decay > 0.5 else "integration_decay"
        }

```