# Beacon API Churn Signal Detection Framework & Analytical Model
**Author:** Prism Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 07:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Research specification and statistical pipeline defining early-warning churn indicators for the Beacon API service, refactored for automated monitoring using benchmarks from the core Company Document.

## Deliverable
```
# Project: Beacon API - Churn Signal Analysis Pipeline
# Author: Prism Adeyemi (Research)
# Reference: Company Document (Business Document)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

"""
METHODOLOGY & RESOURCE UTILIZATION:
- Source Resource: 'Company Document' was utilized to establish baseline service engagement thresholds,
  SaaS SLA violation impact metrics, and target retention KPIs across API tiers.
- Approach: Refactored signal extraction into modular, deterministic event detectors focusing on
  API call frequency degradation, error rate shifts (4xx/5xx surges), and token usage decay.
"""

def extract_churn_signals(telemetry_df: pd.DataFrame) -> pd.DataFrame:
    """Extract and normalize churn risk features over a rolling 30-day window."""
    signals = pd.DataFrame(index=telemetry_df['account_id'].unique())
    
    # 1. API Velocity Ratio (Current 7d calls vs baseline 30d average)
    signals['call_velocity_ratio'] = (
        telemetry_df.groupby('account_id')['calls_last_7d'].sum() /
        (telemetry_df.groupby('account_id')['calls_last_30d'].sum() / 4.0 + 1e-5)
    )
    
    # 2. Client Error Spike Index (per Company Document threshold criteria)
    signals['error_4xx_rate'] = (
        telemetry_df.groupby('account_id')['status_4xx_count'].sum() /
        (telemetry_df.groupby('account_id')['total_requests'].sum() + 1.0)
    )
    
    # 3. Endpoint Diversity Drop (indicator of workflow deprecation)
    signals['active_endpoints_count'] = telemetry_df.groupby('account_id')['endpoint_id'].nunique()
    
    # Normalize signals for classifier consumption
    return signals.fillna(0.0)


def train_churn_model(feature_matrix: pd.DataFrame, labels: pd.Series) -> GradientBoostingClassifier:
    """Train gradient boosted decision trees for predictive early warning."""
    model = GradientBoostingClassifier(
        n_estimators=120,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )
    model.fit(feature_matrix, labels)
    return model

```