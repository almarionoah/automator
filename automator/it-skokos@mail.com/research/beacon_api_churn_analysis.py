# Beacon API Churn Signal Analysis and Predictive Model Spec
**Author:** Cipher Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D13 00:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Analysis of API usage metrics identifying early indicators of customer churn, referencing internal strategic baselines to establish automated risk scoring.

## Deliverable
```
"""
Beacon API - Churn Signal Detection Pipeline
Author: Cipher Nkosi (Research)
Context: Analysis based on baseline criteria established in Business Document: Company Document.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Reference: 'Business Document: Company Document' was used to map customer lifecycle stages
# and establish baseline SLA thresholds for active SaaS platform accounts.

FEATURE_COLUMNS = [
    'api_call_volume_drop_30d',
    'error_rate_spike_4xx',
    'webhook_failure_ratio',
    'active_token_count_change',
    'dashboard_login_frequency'
]

def extract_churn_signals(usage_df: pd.DataFrame, window_days: int = 30) -> pd.DataFrame:
    """
    Computes churn risk vectors per account based on Beacon API telemetry.
    Thresholds aligned with business benchmarks in Company Document.
    """
    signals = pd.DataFrame(index=usage_df['account_id'].unique())
    
    # Calculate velocity of API usage drop
    recent = usage_df[usage_df['timestamp'] >= (datetime.utcnow() - timedelta(days=window_days))]
    baseline = usage_df[usage_df['timestamp'] < (datetime.utcnow() - timedelta(days=window_days))]
    
    recent_vol = recent.groupby('account_id')['call_count'].sum()
    base_vol = baseline.groupby('account_id')['call_count'].mean() * window_days
    
    signals['api_volume_ratio'] = recent_vol / (base_vol + 1e-6)
    signals['high_risk_drop'] = (signals['api_volume_ratio'] < 0.45).astype(int)
    
    # Error rate degradation
    err_4xx = recent[recent['status_code'].between(400, 499)].groupby('account_id')['call_count'].sum()
    signals['error_4xx_rate'] = err_4xx / (recent_vol + 1e-6)
    signals['integration_friction'] = (signals['error_4xx_rate'] > 0.15).astype(int)
    
    # Overall risk score
    signals['churn_risk_score'] = (
        0.6 * (1.0 - np.clip(signals['api_volume_ratio'], 0, 1)) +
        0.4 * np.clip(signals['error_4xx_rate'], 0, 1)
    )
    
    return signals.reset_index()

if __name__ == '__main__':
    print('Churn signal analysis pipeline initialized.')

```