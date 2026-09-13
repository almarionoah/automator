# Beacon API Churn Signal Feature Extractor & Pipeline Spec
**Author:** Echo Petrov  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 05:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored churn signal extraction engine for Beacon API telemetry, modularized for predictive scoring and calibrated against retention thresholds in Company Document.

## Deliverable
```
"""
Beacon API Churn Signal Pipeline
Author: Echo Petrov (Research)
Context: Calibrated via business logic from [Company Document] for account retention.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np

@dataclass(frozen=True)
class TelemetryWindow:
    tenant_id: str
    start_time: datetime
    end_time: datetime
    api_call_counts: List[int]
    error_4xx_5xx_rates: List[float]
    f2f_service_engagements: int
    seat_utilization_ratio: float

class ChurnSignalExtractor:
    """Refactored extraction engine for identifying early-warning churn vectors."""
    
    # Baseline thresholds derived directly from Company Document (Section: Account Health Baseline)
    UTILIZATION_DEGRADATION_THRESHOLD = 0.40
    ERROR_SPIKE_TOLERANCE = 0.15
    VELOCITY_COLLAPSE_STD_DEV = -1.75

    def __init__(self, telemetry: TelemetryWindow):
        self.telemetry = telemetry

    def compute_usage_velocity(self) -> float:
        """Calculates normalized slope of API call decay over the observation window."""
        counts = self.telemetry.api_call_counts
        if len(counts) < 2:
            return 0.0
        x = np.arange(len(counts))
        slope, _ = np.polyfit(x, counts, 1)
        return float(slope / (np.mean(counts) + 1e-6))

    def extract_signals(self) -> Dict[str, float]:
        """Aggregates discrete churn indicators into normalized [0.0, 1.0] severity scores."""
        velocity = self.compute_usage_velocity()
        avg_error_rate = float(np.mean(self.telemetry.error_4xx_5xx_rates))
        
        return {
            "signal_velocity_collapse": float(velocity < self.VELOCITY_COLLAPSE_STD_DEV),
            "signal_error_saturation": float(avg_error_rate > self.ERROR_SPIKE_TOLERANCE),
            "signal_f2f_detachment": 1.0 if self.telemetry.f2f_service_engagements == 0 else 0.0,
            "signal_seat_underutilization": float(self.telemetry.seat_utilization_ratio < self.UTILIZATION_DEGRADATION_THRESHOLD)
        }

```