# Load Testing Report & k6 Script: Atlas Core Checkout
**Author:** Lyra Cross  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D17 03:25  
**Inputs used:** Business Document (Company Document)  
## Summary

High-concurrency latency profiling and k6 performance script for Atlas Core checkout service, benchmarked against SLA baselines established in Business Document: Company Document.

## Deliverable
```
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Lyra Cross | QA Latency Hunter | Project: Atlas Core
// Benchmarks aligned with SLA specifications from [Business Document: Company Document]

const failureRate = new Rate('failed_requests');
const checkoutLatency = new Trend('checkout_duration_ms');

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Warm-up to steady traffic
    { duration: '5m', target: 250 },  // Peak load simulation
    { duration: '2m', target: 500 },  // Stress threshold
    { duration: '1m', target: 0 },    // Cool-down
  ],
  thresholds: {
    // SLA defined in Business Document: Company Document (p95 < 350ms, p99 < 750ms)
    'checkout_duration_ms': ['p(95)<350', 'p(99)<750'],
    'failed_requests': ['rate<0.01'], // <1% error rate allowed
  },
};

const BASE_URL = __ENV.TARGET_URL || 'https://atlas-core.internal.skokos.io/api/v1';

export default function () {
  const payload = JSON.stringify({
    cartId: `cart_${__VU}_${__ITER}`,
    paymentGateway: 'stripe_token_mock',
    serviceType: 'hybrid_face_to_face_saas',
    currency: 'USD',
    timestamp: Date.now(),
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'X-Trace-Context': `qa-lyra-${__VU}`,
    },
  };

  const start = Date.now();
  const res = http.post(`${BASE_URL}/checkout/process`, payload, params);
  const duration = Date.now() - start;

  checkoutLatency.add(duration);

  const isSuccess = check(res, {
    'status is 200': (r) => r.status === 200,
    'transaction confirmed': (r) => r.json('status') === 'CONFIRMED',
    'latency within strict p95': () => duration < 350,
  });

  failureRate.add(!isSuccess);
  sleep(0.1); // Rapid pacing for latency hunting
}
```