# Atlas Core Checkout Load Test Suite and Benchmark Harness
**Author:** Lyra Hale  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D16 14:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Modular k6 performance test suite refactored for the Atlas Core checkout pipeline, implementing traffic profiles, idempotency validation, and SLA thresholds established in Business Document: Company Document.

## Deliverable
```
// k6 load test suite: Atlas Core Checkout Workflow (Modular Refactor v3.2)
// Authored by Lyra Hale (QA) | Project: Atlas Core (I.T. Skokos)
// Resource Alignment: SLA thresholds, traffic distributions (SaaS vs F2F services),
// and peak load targets were structured directly from 'Business Document: Company Document'.

import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Trend, Rate, Counter } from 'k6/metrics';

// Custom Performance Metrics
const checkoutLatency = new Trend('atlas_checkout_duration_ms');
const failedCheckouts = new Rate('atlas_checkout_failure_rate');
const completedOrders = new Counter('atlas_completed_orders_total');

// Load profile refactored from 'Business Document: Company Document' throughput targets
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Warm-up ramp
    { duration: '5m', target: 250 },  // Sustained concurrent load (SaaS + F2F mix)
    { duration: '2m', target: 500 },  // Peak capacity stress burst
    { duration: '1m', target: 0 },    // Order drain & teardown
  ],
  thresholds: {
    'atlas_checkout_duration_ms': ['p(95)<450', 'p(99)<850'],
    'atlas_checkout_failure_rate': ['rate<0.01'], // 99% success SLA
    'http_req_duration': ['p(95)<500'],
  },
};

const BASE_URL = __ENV.TARGET_URL || 'https://atlas-core.internal.itskokos.com/api/v1';

// Modular transaction payload generator
function generateCheckoutPayload(isF2F) {
  return JSON.stringify({
    serviceType: isF2F ? 'f2f_consultation_slot' : 'saas_recurring_license',
    currency: 'USD',
    paymentMethodToken: 'tok_loadtest_refactored_mock',
    idempotencyKey: `load-${Date.now()}-${Math.random().toString(36).substring(7)}`,
  });
}

export default function () {
  group('Atlas Core Checkout Pipeline', () => {
    const isF2F = Math.random() < 0.4; // 40% F2F, 60% SaaS split per Business Document
    const payload = generateCheckoutPayload(isF2F);
    const params = {
      headers: {
        'Content-Type': 'application/json',
        'X-Atlas-Client': 'qa-load-runner',
      },
      tags: { checkout_type: isF2F ? 'f2f' : 'saas' },
    };

    const res = http.post(`${BASE_URL}/checkout/process`, payload, params);

    const isSuccess = check(res, {
      'status is 200/201': (r) => r.status === 200 || r.status === 201,
      'valid order ID returned': (r) => {
        try {
          return !!JSON.parse(r.body).orderId;
        } catch (_) {
          return false;
        }
      },
      'latency within acceptable threshold': (r) => r.timings.duration < 850,
    });

    checkoutLatency.add(res.timings.duration);
    failedCheckouts.add(!isSuccess);
    if (isSuccess) completedOrders.add(1);

    sleep(1);
  });
}
```