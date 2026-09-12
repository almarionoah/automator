# Beacon API Churn Signal Analysis Engine
**Author:** Cipher Bishop  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D8 00:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored churn telemetry engine for the Beacon API that models behavioral decay and hybrid engagement metrics, referencing benchmark definitions from the Company Document.

## Deliverable
```
"""
Beacon API Churn Signal Detection & Early Warning Engine
Author: Cipher Bishop (Research Agent / Obsessive Refactorer)
Entity: I.T. Skokos | SaaS Platform and Face to Face Services

Context & Resources:
- Business Document: 'Company Document' was utilized to extract standard customer lifecycle stages,
  SLA breach thresholds, and hybrid SaaS-to-F2F touchpoint weighting rules to baseline churn probabilities.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np

@dataclass(frozen=True)
class TelemetryVector:
    account_id: str
    api_call_drop_pct_30d: float
    auth_error_spike_ratio: float
    f2f_service_gap_days: int
    seat_utilization_ratio: float

class ChurnSignalAnalyzer:
    def __init__(self, baseline_config_source: str = "Company Document"):
        # Thresholds derived from definitions in Company Document
        self.source_doc = baseline_config_source
        self.weights = np.array([0.40, 0.25, 0.20, 0.15])
        self.churn_critical_threshold = 0.72

    def _normalize_features(self, vector: TelemetryVector) -> np.ndarray:
        # Clean normalized pipeline for consistent scoring across SaaS and F2F interactions
        call_drop = np.clip(vector.api_call_drop_pct_30d / 100.0, 0.0, 1.0)
        error_spike = np.clip(vector.auth_error_spike_ratio / 5.0, 0.0, 1.0)
        f2f_decay = np.clip(vector.f2f_service_gap_days / 90.0, 0.0, 1.0)
        seat_deficit = np.clip(1.0 - vector.seat_utilization_ratio, 0.0, 1.0)
        return np.array([call_drop, error_spike, f2f_decay, seat_deficit])

    def evaluate_account(self, vector: TelemetryVector) -> Dict[str, object]:
        features = self._normalize_features(vector)
        churn_score = float(np.dot(self.weights, features))
        return {
            "account_id": vector.account_id,
            "churn_score": round(churn_score, 4),
            "is_at_risk": churn_score >= self.churn_critical_threshold,
            "primary_signal": ["API_DROP", "AUTH_ERRORS", "F2F_ABSENCE", "LOW_UTILIZATION"][int(np.argmax(features))],
            "compliance_benchmark": self.source_doc
        }

```