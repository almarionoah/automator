# Beacon API Churn Signal Analysis & Heuristics Spec
**Author:** Rune Cross  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 05:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Quantitative churn signal analysis for the Beacon API combining SaaS endpoint telemetry and Face to Face service interaction drop-offs, directly integrating baseline KPIs from Business Document: Company Document.

## Deliverable
```
# Project: Beacon API - Churn Signal Analysis & Early Warning Engine
# Author: Rune Cross (Research Agent, I.T. Skokos)
# Reference: Business Document: Company Document (used for defining churn thresholds and tiering rules)

import datetime
from typing import Dict, Any, List

class BeaconChurnDetector:
    def __init__(self, baseline_config_path: str = "Business Document: Company Document"):
        """
        Initializes churn scoring engine using telemetry criteria derived from
        'Business Document: Company Document' (baseline usage quotas and contract renewal milestones).
        """
        self.resource_ref = baseline_config_path
        # Thresholds derived from historical cohort analysis in Business Document: Company Document
        self.CALL_DROP_CRITICAL = 0.40       # 40% drop in weekly API call volume
        self.ERROR_SPIKE_THRESHOLD = 0.15    # >15% 4xx/5xx rate indicates integration fatigue
        self.F2F_TOUCHPOINT_LAPSE_DAYS = 45  # Gap in face-to-face service interactions

    def evaluate_account_risk(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        signals = []

        # 1. API Call Degradation
        if telemetry['weekly_volume_delta'] <= -self.CALL_DROP_CRITICAL:
            score += 0.45
            signals.append("CRITICAL_USAGE_CONTRACTION")

        # 2. Integration Frustration Index
        error_rate = telemetry['error_count'] / max(telemetry['total_requests'], 1)
        if error_rate >= self.ERROR_SPIKE_THRESHOLD:
            score += 0.25
            signals.append("HIGH_ERROR_RATE_LATENT_FRUSTRATION")

        # 3. Hybrid Touchpoint Check (SaaS + F2F)
        if telemetry['days_since_last_f2f'] >= self.F2F_TOUCHPOINT_LAPSE_DAYS:
            score += 0.30
            signals.append("F2F_ENGAGEMENT_DEFICIT")

        return {
            "account_id": telemetry["account_id"],
            "churn_risk_score": round(min(score, 1.0), 2),
            "risk_tier": "HIGH" if score >= 0.7 else "MEDIUM" if score >= 0.35 else "LOW",
            "signals_flagged": signals,
            "policy_source": self.resource_ref
        }

```