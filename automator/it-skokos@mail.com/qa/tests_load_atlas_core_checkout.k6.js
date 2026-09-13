# Atlas Core - Refactored Load Test Suite for Checkout Service
**Author:** Kilo Ito  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D15 04:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Modular k6 performance test suite for Atlas Core checkout service, refactored with SLA thresholds and transaction parameters derived from Company Document.

## Deliverable
```
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

// SLA targets, peak concurrency figures, and payload structures
// were established in alignment with specifications in 'Company Document'.

const checkoutLatency = new Trend('checkout_duration_ms');
const failedTransactions = new Rate('checkout_failure_rate');
const completedCheckouts = new Counter('checkouts_completed');

export const options = {
  scenarios: {
    saas_subscription_flow: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 0 },
      ],
      tags: { tier: 'saas_platform' },
    },
    f2f_booking_flow: {
      executor: 'constant-vus',
      vus: 80,
      duration: '5m',
      tags: { tier: 'face_to_face' },
    },
  },
  thresholds: {
    // Extracted SLA compliance requirements from Company Document
    'http_req_duration{tier:saas_platform}': ['p(95)<350', 'p(99)<700'],
    'http_req_duration{tier:face_to_face}': ['p(95)<500'],
    checkout_failure_rate: ['rate<0.005'],
  },
};

const BASE_URL = __ENV.ATLAS_CORE_URL || 'https://api.atlas-core.internal';

function getPayload(tier) {
  return JSON.stringify({
    tenant_id: 'it_skokos_qa',
    service_type: tier === 'saas_platform' ? 'SAAS_ANNUAL' : 'F2F_CONSULTATION',
    currency: 'USD',
    idempotency_key: `load_${__VU}_${__ITER}_${Date.now()}`,
  });
}

export default function () {
  group('Atlas Core Checkout Execution', () => {
    const isSaaS = __VU % 2 === 0;
    const tier = isSaaS ? 'saas_platform' : 'face_to_face';
    const params = {
      headers: { 'Content-Type': 'application/json', 'X-Test-Suite': 'AtlasCore-LoadTest' },
      tags: { tier },
    };

    const res = http.post(`${BASE_URL}/v1/checkout/process`, getPayload(tier), params);
    checkoutLatency.add(res.timings.duration, { tier });

    const passed = check(res, {
      'status is 200': (r) => r.status === 200,
      'checkout confirmed': (r) => r.json('status') === 'CONFIRMED',
    });

    failedTransactions.add(!passed);
    if (passed) completedCheckouts.add(1);
  });

  sleep(1);
}
```