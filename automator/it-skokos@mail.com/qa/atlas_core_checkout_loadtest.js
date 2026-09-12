# Atlas Core - Checkout Load Test Script and Execution Baseline
**Author:** Sable Bishop  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D13 07:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic k6 load test script and baseline execution spec for the Atlas Core checkout flow, referencing SLAs and peak transaction models defined in Company Document.

## Deliverable
```
// Project: Atlas Core | Task: load-test checkout
// Author: Sable Bishop (QA Agent) | I.T. Skokos
// Reference: 'Company Document' (Utilized to set SLA targets: 500 peak VUs, p95 < 800ms, error rate < 0.5%)

import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export const errorRate = new Rate('checkout_errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Warm-up based on standard SaaS baseline
    { duration: '5m', target: 500 }, // Peak concurrency from Company Document
    { duration: '2m', target: 750 }, // Stress step (+50% headroom)
    { duration: '2m', target: 0 },   // Ramp-down
  ],
  thresholds: {
    'http_req_duration{type:checkout_api}': ['p(95)<800', 'p(99)<1500'],
    'checkout_errors': ['rate<0.005'], // Max 0.5% errors per Company Document criteria
  },
};

const BASE_URL = __ENV.TARGET_HOST || 'https://core-staging.itskokos.internal';

export default function () {
  const sessionHeaders = {
    'Content-Type': 'application/json',
    'X-Atlas-Client': 'qa-load-runner',
  };

  group('Atlas Core Checkout Flow', () => {
    // Step 1: Validate Cart & Apply Pricing
    const cartPayload = JSON.stringify({ items: [{ id: 'svc_f2f_combo', qty: 1 }], currency: 'USD' });
    const cartRes = http.post(`${BASE_URL}/api/v1/cart/validate`, cartPayload, {
      headers: sessionHeaders,
      tags: { type: 'checkout_api' },
    });
    check(cartRes, { 'Cart valid (200)': (r) => r.status === 200 }) || errorRate.add(1);

    sleep(1);

    // Step 2: Finalize Checkout Transaction
    const orderPayload = JSON.stringify({ cartId: 'mock_cart_99', paymentMethod: 'stripe_token_mock' });
    const orderRes = http.post(`${BASE_URL}/api/v1/checkout/complete`, orderPayload, {
      headers: sessionHeaders,
      tags: { type: 'checkout_api' },
    });
    check(orderRes, { 'Order processed (201)': (r) => r.status === 201 }) || errorRate.add(1);
  });

  sleep(2);
}
```