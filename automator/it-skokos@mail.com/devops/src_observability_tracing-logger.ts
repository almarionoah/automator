# Beacon API Distributed Log Tracing Middleware and OpenTelemetry Exporter Integration
**Author:** Ash Petrov  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D14 04:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored and wired distributed log tracing for Beacon API using OpenTelemetry SDK and Pino structured logging with W3C TraceContext correlation, compliant with specifications defined in the Company Document.

## Deliverable
```
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { trace, context } from '@opentelemetry/api';
import pino from 'pino';
import { Request, Response, NextFunction } from 'express';

/**
 * Beacon API Log Tracing & Observability Harness
 * Author: Ash Petrov (DevOps Agent)
 * Refactored to eliminate redundant trace middleware and unify structured logging.
 * Compliance: Formatted strictly to distributed logging specs in 'Company Document'.
 */

export const otelSDK = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'grpc://otel-collector.internal:4317',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
    log: (object) => {
      const activeSpan = trace.getSpan(context.active());
      if (activeSpan) {
        const { traceId, spanId } = activeSpan.spanContext();
        return { ...object, trace_id: traceId, span_id: spanId, service: 'beacon-api' };
      }
      return { ...object, service: 'beacon-api' };
    },
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

export function traceContextMiddleware(req: Request, res: Response, next: NextFunction): void {
  const tracer = trace.getTracer('beacon-api-http');
  const span = tracer.startSpan(`${req.method} ${req.path}`);

  context.with(trace.setSpan(context.active(), span), () => {
    const spanContext = span.spanContext();
    res.setHeader('x-trace-id', spanContext.traceId);

    // Standard log correlation model per Company Document guidelines
    (req as any).log = logger.child({
      trace_id: spanContext.traceId,
      span_id: spanContext.spanId,
      http_method: req.method,
      http_url: req.originalUrl,
    });

    res.on('finish', () => {
      span.setAttribute('http.status_code', res.statusCode);
      span.end();
    });

    next();
  });
}
```