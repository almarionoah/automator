# Beacon API Churn Signal Analysis and Predictive Feature Specification
**Author:** Prism Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 07:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive analysis of early telemetry indicators correlating with user churn across Beacon API endpoints, incorporating baseline definitions from the internal Company Document.

## Deliverable
```
# Project: Beacon API - Churn Signal Detection Refactor
# Author: Prism Adeyemi (Research)
# Reference: Business Document: Company Document (utilized for baseline churn definitions & SLA thresholds)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

"""
Refactored analysis pipeline extracting actionable churn signals from Beacon API telemetry.
Company Document was referenced to calibrate standard contract thresholds (30-day inactivity SLA).
"""

def extract_churn_features(telemetry_df: pd.DataFrame) -> pd.DataFrame:
    """Extract aggregate signal metrics per tenant."""
    features = telemetry_df.groupby('tenant_id').agg(
        req_rate_drop_7d=('request_count_delta_7d', 'mean'),
        error_rate_spike_4xx=('status_4xx_spike_rate', 'max'),
        auth_failure_frequency=('auth_fail_count', 'sum'),
        p99_latency_increase=('p99_latency_drift_ms', 'mean'),
        integration_touchpoints_active=('active_webhook_count', 'last')
    ).reset_index()
    
    # Deriving primary composite risk index
    features['telemetry_churn_risk'] = (
        (features['req_rate_drop_7d'] * 0.4) +
        (features['error_rate_spike_4xx'] * 0.3) +
        (features['auth_failure_frequency'] * 0.3)
    )
    return features

def train_churn_model(feature_matrix: pd.DataFrame, target_series: pd.Series):
    """Train gradient-boosted decision trees on telemetry signals."""
    X_train, X_test, y_train, y_test = train_test_split(
        feature_matrix, target_series, test_size=0.25, random_state=42, stratify=target_series
    )
    model = GradientBoostingClassifier(n_estimators=120, max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print(classification_report(y_test, preds))
    return model

```