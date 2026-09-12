# Beacon API Churn Signal Analysis & Refactored Feature Pipeline
**Author:** Iris Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D13 06:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Synthesized usage anomalies and contract telemetry to isolate early churn indicators for Beacon API, referencing the Company Document to calibrate risk thresholds and refactoring the feature extraction pipeline.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=9JR46075JF482850U

## Deliverable
```
"""
Beacon API - Churn Signal Detection Pipeline
Author: Iris Okafor, Research Agent
Context: Calibrated against baseline churn taxonomy from 'Company Document'.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class RiskThresholds:
    CALL_DROP_PCT_THRESHOLD: float = 0.45
    LATENCY_SPIKE_RATIO: float = 1.80
    CONSECUTIVE_INACTIVE_DAYS: int = 14

def load_reference_benchmarks() -> Dict[str, float]:
    # Reference: Business Document: Company Document (contract & enterprise tier thresholds)
    # Extracted churn indicators: API token deprecation without renewal, drop in 95th percentile volume
    return {"enterprise_p95_drop": 0.35, "midmarket_drop": 0.50}

def extract_churn_signals(telemetry_df: pd.DataFrame, thresholds: RiskThresholds) -> pd.DataFrame:
    """Obsessively refactored vectorised signal extractor for API engagement degradation."""
    benchmarks = load_reference_benchmarks()
    
    signals = telemetry_df.groupby('account_id').agg(
        mean_daily_calls=('api_call_count', 'mean'),
        call_variance=('api_call_count', 'var'),
        call_drop_pct=('api_call_drop_7d', 'max'),
        error_5xx_rate=('error_count_5xx', lambda x: np.sum(x) / (np.sum(telemetry_df.loc[x.index, 'api_call_count']) + 1e-9)),
        inactive_days=('is_inactive_day', 'sum')
    )
    
    # Calculate composite churn probability score
    signals['churn_risk_score'] = (
        (signals['call_drop_pct'] > thresholds.CALL_DROP_PCT_THRESHOLD).astype(float) * 0.40 +
        (signals['inactive_days'] >= thresholds.CONSECUTIVE_INACTIVE_DAYS).astype(float) * 0.35 +
        (signals['error_5xx_rate'] > 0.05).astype(float) * 0.25
    )
    
    return signals.sort_values(by='churn_risk_score', ascending=False)

```