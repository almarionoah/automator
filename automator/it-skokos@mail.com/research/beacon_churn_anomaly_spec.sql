# Beacon API Churn Signal Boundary Analysis and Telemetry Rule Spec
**Author:** Pixel Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D14 07:10  
**Inputs used:** Business Document (Company Document)  
## Summary

An edge-case research specification identifying non-linear churn telemetry signals in the Beacon API, benchmarked against tier definitions from Company Document.

## Deliverable
```
-- Research Artefact: Beacon API Churn Telemetry & Edge-Case Anomaly Detection
-- Author: Pixel Fontaine (Research Agent / Edge-Case Archaeologist)
-- Reference: Business Document: Company Document (used to extract baseline SLA thresholds, tier-based API quotas, and contractual renewal trigger windows).

WITH BaselineTelemetry AS (
    SELECT 
        account_id,
        tier_level, -- Mapped directly from Business Document: Company Document
        DATE_TRUNC('day', request_timestamp) AS usage_date,
        COUNT(CASE WHEN response_status = 200 THEN 1 END) AS successful_calls,
        COUNT(CASE WHEN response_status IN (401, 403) THEN 1 END) AS auth_failures,
        COUNT(CASE WHEN response_status = 429 THEN 1 END) AS rate_limits,
        AVG(latency_ms) AS avg_latency,
        COUNT(DISTINCT user_agent) AS client_fingerprints
    FROM beacon_api_gateway_logs
    WHERE request_timestamp >= NOW() - INTERVAL '90 days'
    GROUP BY 1, 2, 3
),
EdgeCaseChurnPatterns AS (
    SELECT 
        account_id,
        tier_level,
        -- Anomaly 1: Token Rotations without Traffic (Pre-migration testing)
        SUM(auth_failures) FILTER (WHERE usage_date >= NOW() - INTERVAL '14 days') AS recent_auth_spikes,
        -- Anomaly 2: Silent Degradation (Sudden drop to single-threaded ping/health checks only)
        AVG(successful_calls) FILTER (WHERE usage_date >= NOW() - INTERVAL '7 days') / 
            NULLIF(AVG(successful_calls) FILTER (WHERE usage_date BETWEEN NOW() - INTERVAL '60 days' AND NOW() - INTERVAL '30 days'), 0) AS traffic_velocity_ratio,
        -- Anomaly 3: SDK Fingerprint Pruning (Deprecating Beacon API from secondary microservices)
        MAX(client_fingerprints) FILTER (WHERE usage_date <= NOW() - INTERVAL '30 days') - 
            MAX(client_fingerprints) FILTER (WHERE usage_date >= NOW() - INTERVAL '7 days') AS dropped_integrations
    FROM BaselineTelemetry
    GROUP BY 1, 2
)
SELECT 
    account_id,
    tier_level,
    CASE 
        WHEN traffic_velocity_ratio < 0.15 AND dropped_integrations >= 2 THEN 'CRITICAL_SILENT_MIGRATION'
        WHEN recent_auth_spikes > 50 AND traffic_velocity_ratio < 0.50 THEN 'AUTH_DECOMMISSIONING_RISK'
        ELSE 'MONITOR'
    END AS churn_risk_classification
FROM EdgeCaseChurnPatterns
WHERE traffic_velocity_ratio < 0.50 OR recent_auth_spikes > 50;
```