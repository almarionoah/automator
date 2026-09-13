# Atlas Core Checkout Load Test Suite (k6)
**Author:** Torq Bishop  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D17 08:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready k6 load testing script and scenario execution profile for Atlas Core checkout endpoints, configured against SLA baselines and peak throughput models defined in Business Document: Company Document.

## Deliverable
```
// Torq Bishop | QA - Atlas Core Checkout Load Test
// Reference: 'Business Document: Company Document' (Used to derive SLA thresholds: p95 < 650ms, peak 450 RPS, and hybrid SaaS/Face-to-Face cart structures)

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('checkout_failures');

export const options = {
  scenarios: {
    checkout_ramp: {
      executor: 'ramping-arrival-rate',
      startRate: 50,
      timeUnit: '1s',
      preAllocatedVUs: 100,
      maxVUs: 600,
      stages: [
        { duration: '2m', target: 150 }, // Normal SaaS + In-Person booking load
        { duration: '5m', target: 450 }, // Peak burst per Company Document SLA
        { duration: '2m', target: 50 },  // Cool down
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<650', 'p(99)<1200'], // Mandated by Business Document: Company Document
    checkout_failures: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.ATLAS_CORE_URL || 'https://api.skokos.internal/v1';

export default function () {
  const payload = JSON.stringify({
    account_id: `act_${__VU}_${__ITER}`,
    cart_type: __ITER % 2 === 0 ? 'saas_subscription' : 'f2f_service_booking',
    items: [
      {
        sku: 'SKK-CORE-PRO',
        quantity: 1,
        unit_price_cents: 9900,
      },
    ],
    payment_token: 'tok_load_test_mock',
    idempotency_key: `idemp_${__VU}_${Date.now()}_${Math.random()}`,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'X-Client-Platform': 'I.T. Skokos SaaS Engine',
    },
  };

  const res = http.post(`${BASE_URL}/checkout/process`, payload, params);
  const success = check(res, {
    'status is 200/201': (r) => r.status === 200 || r.status === 201,
    'order_id returned': (r) => JSON.parse(r.body).order_id !== undefined,
  });

  errorRate.add(!success);
  sleep(1);
}
```