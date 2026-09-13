# Beacon API Churn Signal Chaos & Vulnerability Assessment
**Author:** Nova Cross  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 08:55  
**Inputs used:** Business Document (Company Document)  
## Summary

A chaos engineering test harness and telemetry script designed to simulate API failure modes, detect leading churn indicators, and correlate drop-off metrics against baselines defined in Business Document: Company Document.

## Deliverable
```
"""
Beacon API - Churn Signal & Fault Injection Test Harness
Author: Nova Cross (Chaos Research, I.T. Skokos)
Resource Reference: 'Business Document: Company Document' (utilized to baseline acceptable SLA thresholds, standard customer interaction intervals, and core account deactivation triggers).
"""

import time
import random
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CHAOS-EXPERIMENT] - %(message)s')

class ChurnSignalChaosTester:
    def __init__(self, target_api_url: str):
        self.target_api_url = target_api_url
        # Baseline metrics ingested from Business Document: Company Document
        self.sla_latency_threshold_ms = 450.0
        self.error_rate_churn_trigger = 0.08  # >8% sustained errors indicates high churn risk
        self.heartbeat_timeout_seconds = 14

    def inject_latency_jitter(self, request_payload: dict) -> dict:
        """Simulates downstream dependency degradation to measure customer retry fatigue."""
        induced_delay = random.uniform(0.1, 1.2)
        time.sleep(induced_delay)
        
        status_code = 504 if induced_delay * 1000 > self.sla_latency_threshold_ms else 200
        return {"status": status_code, "latency_ms": round(induced_delay * 1000, 2), "payload": request_payload}

    def evaluate_churn_risk(self, telemetry_window: list) -> dict:
        """Correlates failure metrics with churn indicators detailed in Company Document."""
        total_requests = len(telemetry_window)
        failures = sum(1 for res in telemetry_window if res['status'] >= 500)
        failure_rate = failures / total_requests if total_requests else 0.0
        
        churn_signal_detected = failure_rate > self.error_rate_churn_trigger
        return {
            "total_events": total_requests,
            "failure_rate": round(failure_rate, 4),
            "churn_signal_alert": churn_signal_detected,
            "recommendation": "Trigger proactive account engagement" if churn_signal_detected else "Nominal"
        }

if __name__ == '__main__':
    tester = ChurnSignalChaosTester('https://api.itskokos.internal/beacon/v1')
    sample_events = [tester.inject_latency_jitter({'client_id': f'cli_{i}'}) for i in range(25)]
    print(json.dumps(tester.evaluate_churn_risk(sample_events), indent=2))
```