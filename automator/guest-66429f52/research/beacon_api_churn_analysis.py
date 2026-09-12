# Beacon API Churn Signal Analysis & Early Warning Pipeline Spec
**Author:** Cipher Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D144 01:30  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Research specification and analysis pipeline script identifying leading indicators of customer churn for the Beacon API service, utilizing GitHub API telemetry.

## Deliverable
```
"""
Beacon API Churn Signal Analysis Pipeline
Author: Cipher Nkosi (Research Agent)
Project: Beacon API

Authentication & Resource Configuration:
- Git Access: Personal Access Token (PAT) used for querying repository activity, issue tracking, and client telemetry modules via authenticated HTTPS.
- Credentials: Git Hub Personal Access Token utilized to access GitHub Enterprise REST/GraphQL APIs for audit logs, client webhook failures, and repository commit drops.
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

# Configure resources
GIT_PAT = os.getenv("GIT_ACCESS_PERSONAL_ACCESS_TOKEN")
GITHUB_PAT = os.getenv("CREDENTIALS_GITHUB_PERSONAL_ACCESS_TOKEN")

def extract_churn_signals(telemetry_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes churn indicators across API usage, error rates, and support interactions.
    """
    features = pd.DataFrame()
    
    # 1. API Call Velocity Decay (30d rolling vs previous 30d)
    features['call_decay_rate'] = telemetry_df['calls_last_30d'] / (telemetry_df['calls_prev_30d'] + 1e-5)
    
    # 2. 4xx/5xx Error Spike Indicator
    features['error_rate'] = telemetry_df['error_count_30d'] / (telemetry_df['calls_last_30d'] + 1e-5)
    
    # 3. Webhook Latency & Failure Metric
    features['webhook_failure_ratio'] = telemetry_df['failed_webhooks'] / (telemetry_df['total_webhooks'] + 1e-5)
    
    # 4. Developer Activity Drop
    features['active_key_count'] = telemetry_df['active_api_keys']
    
    return features

def train_churn_model(X: pd.DataFrame, y: pd.Series) -> GradientBoostingClassifier:
    """Trains a baseline early warning model for churn detection."""
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(X, y)
    return model

```