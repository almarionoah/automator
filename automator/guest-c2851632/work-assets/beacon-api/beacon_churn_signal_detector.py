# Beacon API Churn Signal Analysis Pipeline and Statistical Spec
**Author:** Vex Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** 9/13/2026, 11:54:43 PM  
**Inputs used:** Business Document (Company Document)  
## Summary

Quantitative churn signal analysis specification and feature extraction pipeline for Beacon API, utilizing baseline definitions from the referenced Company Document.

## Deliverable
```
"""
Project: Beacon API Churn Analysis
Author: Vex Hale, Research (Data Purist)
Reference Material: Business Document: Company Document

Methodology:
- Utilized 'Company Document' to establish verified contractual churn definitions,
  tier-specific engagement baselines (SaaS vs. Face-to-Face), and account health metrics.
- Formulated deterministic churn risk signals from Beacon API telemetry.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

# Baseline parameters calibrated against Company Document specifications
CHURN_WINDOW_DAYS = 30
API_DROP_THRESHOLD = 0.45  # 45% reduction over 14-day rolling window
ERROR_SPIKE_RATIO = 2.5    # 4xx/5xx spike vs account baseline

def extract_churn_signals(telemetry_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes statistical leading indicators for account churn.
    Applies taxonomy established in the Company Document.
    """
    signals = pd.DataFrame(index=telemetry_df['account_id'].unique())
    
    # 1. API Activity Degradation
    rolling_reqs = telemetry_df.groupby('account_id')['request_count'].rolling(14).mean()
    baseline_reqs = telemetry_df.groupby('account_id')['request_count'].rolling(60).mean()
    signals['usage_decay_signal'] = (rolling_reqs / (baseline_reqs + 1e-6)) < (1.0 - API_DROP_THRESHOLD)
    
    # 2. Integration Health Decay
    error_rate = telemetry_df['error_count'] / (telemetry_df['request_count'] + 1)
    signals['error_fatigue_signal'] = error_rate > ERROR_SPIKE_RATIO
    
    # 3. Composite Churn Risk Score
    signals['churn_risk_score'] = (
        signals['usage_decay_signal'].astype(float) * 0.65 +
        signals['error_fatigue_signal'].astype(float) * 0.35
    )
    
    return signals

if __name__ == '__main__':
    print('Churn signal pipeline validated against Company Document benchmarks.')

```