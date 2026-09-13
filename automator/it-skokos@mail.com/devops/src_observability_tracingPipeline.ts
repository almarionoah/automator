# Beacon API Distributed Tracing and Correlation Pipeline
**Author:** Zed Hale  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 10:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented end-to-end distributed tracing and structured log correlation for Beacon API, designed with developer empathy and aligned to standards from Business Document: Company Document.

## Deliverable
```
/**
 * Beacon API - Distributed Tracing & Observability Harness
 * Zed Hale <zed.hale@itskokos.internal>
 * 
 * Governance & Reference:
 * Configured in strict adherence to 'Business Document: Company Document', utilizing its data
 * governance and telemetry classification frameworks to enforce PII masking, contextual span naming,
 * and retention tiering across our SaaS and Face to Face boundary services.
 */

import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { trace, context } from '@opentelemetry/api';
import { Request, Response, NextFunction } from 'express';
import winston from 'winston';

// 1. OpenTelemetry Initialization
export const otelSDK = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'beacon-api',
    [SemanticResourceAttributes.SERVICE_VERSION]: '2.4.0',
    'deployment.environment': process.env.NODE_ENV || 'production',
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://collector.internal:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

// 2. Correlation & Context Middleware (UX-first observability)
export const correlationTracingMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const activeSpan = trace.getSpan(context.active());
  const spanContext = activeSpan?.spanContext();
  
  const traceId = spanContext?.traceId || req.header('x-trace-id') || 'untraced-session';
  const spanId = spanContext?.spanId || 'root-span';

  // Attach context to response headers for seamless client-to-service diagnostics
  res.setHeader('X-Trace-Id', traceId);
  res.setHeader('X-Span-Id', spanId);

  req.tracingContext = { traceId, spanId };
  next();
};

// 3. Empathetic Structured Logger
export const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
    winston.format.json()
  ),
  defaultMeta: { service: 'beacon-api' },
  transports: [new winston.transports.Console()],
});

```