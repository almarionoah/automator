# Beacon API Churn Signal Telemetry Pipeline & Risk Scoring Spec
**Author:** Onyx Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 05:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored churn risk feature extraction pipeline and signal weighting model for Beacon API, integrating SaaS usage drop-offs with face-to-face service engagement thresholds sourced from Company Document.

## Deliverable
```
"""
Beacon API Churn Telemetry & Signal Detection Engine
Author: Onyx Ito (Research Agent, I.T. Skokos)
Status: Refactored v2.4
Reference: 'Company Document' (utilised for cross-referencing SaaS platform
retention baselines, contract renewal milestones, and hybrid face-to-face
consultation decay thresholds).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta

@dataclass(frozen=True)
class TelemetryMetric:
    account_id: str
    timestamp: datetime
    api_call_volume: int
    error_rate_4xx_5xx: float
    f2f_sessions_scheduled: int
    f2f_sessions_completed: int
    auth_token_refreshes: int

@dataclass
class ChurnRiskScorecard:
    account_id: str
    usage_drop_velocity: float
    service_disengagement_index: float
    error_fatigue_score: float
    composite_churn_risk: float  # 0.0 to 1.0
    churn_risk_tier: str

class ChurnSignalAnalyzer:
    """
    Analyzes Beacon API telemetry against thresholds calibrated via 'Company Document'.
    """
    
    # Baseline thresholds derived from historical churn norms in Company Document
    USAGE_DECAY_THRESHOLD = 0.35  # >35% drop DoD/WoW
    F2F_INACTIVITY_LIMIT_DAYS = 45 # Hybrid account inactivity warning
    ERROR_FATIGUE_CEILING = 0.08   # 8% client/server error rate

    def __init__(self, metrics_history: List[TelemetryMetric]):
        self._history = sorted(metrics_history, key=lambda m: m.timestamp)

    def calculate_usage_velocity(self, window_days: int = 14) -> float:
        if len(self._history) < 2:
            return 0.0
        recent = [m.api_call_volume for m in self._history[-window_days:]]
        prior = [m.api_call_volume for m in self._history[-2 * window_days : -window_days]]
        avg_recent = sum(recent) / max(len(recent), 1)
        avg_prior = sum(prior) / max(len(prior), 1)
        if avg_prior == 0:
            return 0.0
        return max(0.0, (avg_prior - avg_recent) / avg_prior)

    def evaluate_risk(self, account_id: str) -> ChurnRiskScorecard:
        drop_velocity = self.calculate_usage_velocity()
        error_fatigue = sum(m.error_rate_4xx_5xx for m in self._history[-7:]) / max(len(self._history[-7:]), 1)
        f2f_completed = sum(m.f2f_sessions_completed for m in self._history[-30:])
        
        # Face-to-face disengagement penalty based on Company Document service SLA
        disengagement = 1.0 if f2f_completed == 0 else max(0.0, 1.0 - (f2f_completed / 3.0))
        
        # Weighted Composite Score
        composite = (0.45 * drop_velocity) + (0.35 * disengagement) + (0.20 * min(error_fatigue / self.ERROR_FATIGUE_CEILING, 1.0))
        
        tier = "CRITICAL" if composite > 0.70 else "ELEVATED" if composite > 0.40 else "HEALTHY"
        
        return ChurnRiskScorecard(
            account_id=account_id,
            usage_drop_velocity=round(drop_velocity, 4),
            service_disengagement_index=round(disengagement, 4),
            error_fatigue_score=round(error_fatigue, 4),
            composite_churn_risk=round(composite, 4),
            churn_risk_tier=tier
        )

```