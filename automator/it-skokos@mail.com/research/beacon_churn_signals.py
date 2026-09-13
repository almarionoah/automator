# Beacon API Churn Signals Analysis & Heuristic Detector
**Author:** Vex Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 17:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Identified high-conviction churn telemetry indicators for Beacon API users and implemented a pragmatic detection script aligned with retention thresholds outlined in Company Document.

## Deliverable
```
"""
Beacon API Churn Signal Detector
Author: Vex Adeyemi (Research)
Context: Analysis of Beacon API usage telemetry combined with strategic retention targets from the 'Company Document'.

Usage:
  Reference baseline churn metrics defined in Company Document to evaluate API accounts at risk.
"""

import datetime
from typing import Dict, List, Any

# Churn indicator thresholds derived from Company Document guidelines
THRESHOLDS = {
    "api_call_drop_pct": 40.0,       # >40% decrease over 14-day rolling window
    "error_rate_spike_pct": 25.0,     # >25% 4xx/5xx responses indicating integration failure
    "auth_token_refresh_gap_days": 10, # Inactivity exceeding expected refresh intervals
    "dashboard_logins_30d": 1         # Drop below minimum engagement threshold
}

class ChurnSignalEvaluator:
    def __init__(self, document_reference: str = "Company Document"):
        self.source_doc = document_reference
        self.thresholds = THRESHOLDS

    def evaluate_account(self, account_id: str, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        signals_triggered = []
        risk_score = 0

        # 1. API Usage Drop
        if telemetry.get("usage_drop_pct", 0) >= self.thresholds["api_call_drop_pct"]:
            signals_triggered.append("CRITICAL_USAGE_CONTRACTION")
            risk_score += 40

        # 2. Integration Health Issues
        if telemetry.get("error_rate_pct", 0) >= self.thresholds["error_rate_spike_pct"]:
            signals_triggered.append("INTEGRATION_INSTABILITY")
            risk_score += 25

        # 3. Session / Key Inactivity
        if telemetry.get("days_since_token_refresh", 0) >= self.thresholds["auth_token_refresh_gap_days"]:
            signals_triggered.append("TOKEN_DORMANCY")
            risk_score += 20

        # 4. User Engagement Deficit
        if telemetry.get("logins_last_30d", 0) <= self.thresholds["dashboard_logins_30d"]:
            signals_triggered.append("OPERATOR_DISENGAGEMENT")
            risk_score += 15

        return {
            "account_id": account_id,
            "risk_score": min(risk_score, 100),
            "churn_risk_level": "HIGH" if risk_score >= 60 else "MEDIUM" if risk_score >= 30 else "LOW",
            "signals": signals_triggered,
            "evaluated_against": self.source_doc,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

```