# Beacon API Distributed Tracing & Log Masking Pipeline
**Author:** Zed Ito  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D11 21:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Secure distributed tracing and structured log pipeline implementation for Beacon API, featuring automated PII redaction, token stripping, and secure span propagation in accordance with compliance guidelines.

## Deliverable
```
// Project: Beacon API - Distributed Tracing Instrumentation
// Author: Zed Ito (DevOps)
// Security Reference: Business Document: Company Document (Used to extract compliance thresholds, mandatory trace attribute filtering, and zero-trust logging mandates for SaaS/F2F transactions).

import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { redactionProcessor } from './redactionProcessor';

const SENSITIVE_HEADERS = ['authorization', 'x-api-key', 'cookie', 'set-cookie', 'x-user-ssn'];
const PII_REGEX = [/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/g, /\b\d{3}-\d{2}-\d{4}\b/g];

// Verified against standards defined in 'Business Document: Company Document' to avoid secret leakage
export const otelSdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'https://collector-internal.itskokos.local:4318/v1/traces',
    headers: { 'X-Security-Zone': 'Internal-SaaS-Core' },
  }),
  spanProcessor: redactionProcessor({
    sanitizeAttributes: (key, value) => {
      if (SENSITIVE_HEADERS.includes(key.toLowerCase())) return '[REDACTED_SECRET]';
      if (typeof value === 'string') {
        return PII_REGEX.reduce((acc, regex) => acc.replace(regex, '[REDACTED_PII]'), value);
      }
      return value;
    },
  }),
  instrumentations: [getNodeAutoInstrumentations({
    '@opentelemetry/instrumentation-http': {
      ignoreIncomingRequestHook: (req) => req.url?.includes('/healthz'),
      requestHook: (span, req) => {
        span.setAttribute('peer.service', 'beacon-api');
        span.setAttribute('compliance.policy', 'BUSINESS_DOC_COMPANY_DOCUMENT_V2');
      }
    }
  })]
});

otelSdk.start();

```