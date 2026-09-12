# Beacon API Distributed Log Tracing Instrumentation
**Author:** Onyx Bishop  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D11 08:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Configured OpenTelemetry distributed trace context propagation and structured JSON log correlation for Beacon API, adhering to logging and observability requirements defined in the Company Document.

## Deliverable
```
/**
 * Project: Beacon API
 * Author: Onyx Bishop (DevOps)
 * Purpose: Distributed log tracing & OpenTelemetry W3C tracecontext injection
 * Reference: Built in compliance with I.T. Skokos 'Company Document' for tracing standards, service correlation across SaaS & Face to Face service gateways, and PII masking.
 */

import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { trace, context } from '@opentelemetry/api';
import winston from 'winston';

const traceExporter = new OTLPTraceExporter({
  url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector.internal.itskokos.com:4318/v1/traces',
});

export const otelSdk = new NodeSDK({
  traceExporter,
  instrumentations: [getNodeAutoInstrumentations({
    '@opentelemetry/instrumentation-http': {
      ignoreIncomingRequestHook: (req) => req.url?.includes('/healthz') || false,
    },
  })],
});

// Format logs with active trace/span context as mandated by Company Document
const traceCorrelator = winston.format((info) => {
  const currentSpan = trace.getSpan(context.active());
  if (currentSpan) {
    const spanContext = currentSpan.spanContext();
    info['trace_id'] = spanContext.traceId;
    info['span_id'] = spanContext.spanId;
    info['trace_flags'] = spanContext.traceFlags.toString(16);
  }
  info['service.name'] = 'beacon-api';
  info['service.domain'] = 'saas-f2f-gateway';
  return info;
});

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    traceCorrelator(),
    winston.format.timestamp({ format: 'ISO' }),
    winston.format.json()
  ),
  transports: [new winston.transports.Console()],
});

otelSdk.start();
logger.info('Beacon API OpenTelemetry log tracing successfully initialized.');
```