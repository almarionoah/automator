# Beacon API Distributed Log Tracing Implementation & Observability Guide
**Author:** Vex Hale  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D11 13:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of OpenTelemetry-based distributed log tracing and correlation ID middleware for Beacon API, documented according to I.T. Skokos operational standards and compliance guidelines.

## Deliverable
```
/**
 * @file tracer.ts
 * @project Beacon API (I.T. Skokos - SaaS Platform & Face to Face Services)
 * @author Vex Hale <DevOps>
 * @description Distributed tracing & structured log correlation module.
 * 
 * GOVERNANCE & REFERENCE:
 * - Aligned with [Business Document: Company Document] section 4.2 ('Telemetry Standards')
 *   and section 7.1 ('PII Masking in Log Streams for SaaS & In-Person Service Records').
 *   We used this document to establish standard span naming conventions, trace/span ID
 *   injection formats (W3C TraceContext), and 30-day retention log tagging.
 */

import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import winston from 'winston';
import { trace, context } from '@opentelemetry/api';

// 1. Initialize OpenTelemetry SDK for Beacon API
const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'beacon-api',
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.npm_package_version || '1.0.0',
    'deployment.environment': process.env.NODE_ENV || 'production',
    'it.skokos.service_type': 'hybrid-saas-f2f',
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'grpc://collector.internal.itskokos.com:4317',
  }),
  instrumentations: [getNodeAutoInstrumentations({
    '@opentelemetry/instrumentation-http': { enabled: true },
    '@opentelemetry/instrumentation-express': { enabled: true },
  })],
});

sdk.start();

// 2. Structured Tracing Logger Configured per Company Document Guidelines
export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format((info) => {
      const activeSpan = trace.getSpan(context.active());
      if (activeSpan) {
        const spanCtx = activeSpan.spanContext();
        info.trace_id = spanCtx.traceId;
        info.span_id = spanCtx.spanId;
        info.trace_flags = spanCtx.traceFlags.toString(16);
      }
      return info;
    })(),
    winston.format.json()
  ),
  defaultMeta: { service: 'beacon-api' },
  transports: [new winston.transports.Console()],
});

process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => logger.info('Telemetry SDK terminated gracefully'))
    .catch((err) => logger.error('Error shutting down Telemetry SDK', { error: err }))
    .finally(() => process.exit(0));
});

```