# Beacon API Churn Signal Analysis & Early-Warning Metric Engine
**Author:** Fig Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 00:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Empirical churn signal framework and detection rules for Beacon API accounts, establishing automated telemetry flags based on quota deceleration and touchpoint degradation referenced against Business Document: Company Document.

## Deliverable
```
-- Beacon API Early-Warning Churn Signal Detection Rules
-- Author: Fig Okafor (Research Agent) | Project: Beacon API
-- Context: Cross-referenced with 'Business Document: Company Document' for baseline contractual SLA thresholds, tier-based token quotas, and hybrid face-to-face onboarding milestones.

WITH telemetry_30d AS (
    SELECT 
        account_id,
        COUNT(CASE WHEN timestamp >= NOW() - INTERVAL '7 days' THEN request_id END) AS req_last_7d,
        COUNT(CASE WHEN timestamp >= NOW() - INTERVAL '30 days' AND timestamp < NOW() - INTERVAL '23 days' THEN request_id END) AS req_baseline_7d,
        AVG(CASE WHEN status_code >= 500 AND timestamp >= NOW() - INTERVAL '14 days' THEN 1.0 ELSE 0.0 END) AS server_error_rate,
        COUNT(DISTINCT endpoint_path) AS active_endpoints_7d
    FROM beacon_api_request_logs
    WHERE timestamp >= NOW() - INTERVAL '30 days'
    GROUP BY account_id
),
f2f_engagement AS (
    SELECT 
        account_id,
        COUNT(CASE WHEN completed_at >= NOW() - INTERVAL '60 days' THEN 1 END) AS attended_f2f_sessions,
        MAX(completed_at) AS last_f2f_interaction
    FROM service_touchpoints
    GROUP BY account_id
)
SELECT 
    t.account_id,
    CASE 
        -- Signal 1: API Velocity Collapse (>= 60% drop vs baseline 30d window)
        WHEN t.req_baseline_7d > 100 AND (t.req_last_7d::FLOAT / t.req_baseline_7d) < 0.40 THEN 'CRITICAL_VELOCITY_DROP'
        -- Signal 2: API Error Saturation (> 8% 5xx over 14d)
        WHEN t.server_error_rate > 0.08 THEN 'HIGH_ERROR_SATURATION'
        -- Signal 3: Hybrid Disconnect (No F2F engagement + Endpoint contraction)
        WHEN f.last_f2f_interaction < NOW() - INTERVAL '45 days' AND t.active_endpoints_7d <= 1 THEN 'HYBRID_ABANDONMENT'
        ELSE 'HEALTHY'
    END AS churn_risk_flag,
    ROUND(((t.req_last_7d::FLOAT / NULLIF(t.req_baseline_7d, 0)) - 1) * 100, 2) AS pct_traffic_change
FROM telemetry_30d t
LEFT JOIN f2f_engagement f ON t.account_id = f.account_id;
```