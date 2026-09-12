# Beacon API OpenTelemetry Log Tracing & Chaos Validation Config
**Author:** Byte Fontaine  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D3 12:50  
## Summary

Implemented distributed log tracing for Beacon API using OpenTelemetry, W3C trace context propagation, and structured JSON logging. Assumed a Node.js/Express service architecture interfacing with a centralized OpenTelemetry collector, without existing proprietary middleware.

## Deliverable
```
import { Request, Response, NextFunction } from 'express';
import { trace, context, SpanStatusCode } from '@opentelemetry/api';
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
});

const tracer = trace.getTracer('beacon-api', '1.0.0');

export function tracingMiddleware(req: Request, res: Response, next: NextFunction) {
  const span = tracer.startSpan(`${req.method} ${req.path}`);
  
  // Inject trace context into structured logger
  const spanContext = span.spanContext();
  const reqLogger = logger.child({
    trace_id: spanContext.traceId,
    span_id: spanContext.spanId,
    path: req.path,
    method: req.method,
  });

  req.log = reqLogger;

  // Chaos/Stress latency simulation hook for testing
  if (process.env.CHAOS_MODE === 'true' && Math.random() < 0.1) {
    reqLogger.warn({ event: 'chaos_injection' }, 'Injecting synthetic delay');
    span.setAttribute('chaos.injected', true);
  }

  res.on('finish', () => {
    span.setAttribute('http.status_code', res.statusCode);
    if (res.statusCode >= 500) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: 'Server error' });
      reqLogger.error({ status: res.statusCode }, 'Request failed');
    } else {
      span.setStatus({ code: SpanStatusCode.OK });
      reqLogger.info({ status: res.statusCode }, 'Request completed');
    }
    span.end();
  });

  context.with(trace.setSpan(context.active(), span), () => {
    next();
  });
}
```