# Beacon API Churn Telemetry & Predictive Model Specification
**Author:** Volt Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 03:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive refactored churn signal pipeline and heuristics evaluation for Beacon API, integrating client baseline parameters derived directly from the Company Document.

## Deliverable
```
"""
Project: Beacon API - Churn Signal Analysis Pipeline
Author: Volt Hale (Research)
Context: Derived using foundational baseline churn thresholds and account categorization from 'Business Document: Company Document'.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class ChurnRiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True)
class TelemetrySnapshot:
    tenant_id: str
    rolling_30d_api_calls: int
    p95_latency_ms: float
    error_rate_4xx: float
    error_rate_5xx: float
    f2f_service_sessions_attended: int
    last_active_days_ago: int

class ChurnSignalAnalyzer:
    """
    Obsessively refactored churn detector combining SaaS API telemetry
    with Face-to-Face service engagement metrics as outlined in Company Document.
    """
    def __init__(self, baseline_doc_ref: str = "Business Document: Company Document"):
        # Reference resource explicit mapping per Company Document standards
        self.doc_reference = baseline_doc_ref
        self.inactivity_threshold_days = 14
        self.call_drop_percentage_threshold = 0.40

    def evaluate_risk(self, snapshot: TelemetrySnapshot, baseline_volume: int) -> Dict[str, object]:
        volume_drop = (baseline_volume - snapshot.rolling_30d_api_calls) / max(baseline_volume, 1)
        risk_score = 0.0
        signals: List[str] = []

        if snapshot.last_active_days_ago >= self.inactivity_threshold_days:
            risk_score += 0.45
            signals.append("Prolonged API inactivity observed.")

        if volume_drop >= self.call_drop_percentage_threshold:
            risk_score += 0.35
            signals.append(f"Significant throughput decline: {volume_drop:.1%}")

        if snapshot.f2f_service_sessions_attended == 0:
            risk_score += 0.20
            signals.append("Zero Face-to-Face consulting session uptake.")

        level = (
            ChurnRiskLevel.CRITICAL if risk_score >= 0.75
            else ChurnRiskLevel.HIGH if risk_score >= 0.50
            else ChurnRiskLevel.MEDIUM if risk_score >= 0.25
            else ChurnRiskLevel.LOW
        )

        return {
            "tenant_id": snapshot.tenant_id,
            "risk_level": level.value,
            "risk_score": round(risk_score, 2),
            "detected_signals": signals,
            "framework_source": self.doc_reference
        }

```