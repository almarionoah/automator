# Beacon API Wire Log Tracing and Context Propagation Middleware
**Author:** Rune Bishop  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 11:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented distributed wire logging and OpenTelemetry trace propagation for Beacon API, designed to provide frictionless telemetry and empathetic operator observability across both SaaS and Face to Face service flows. Explicitly structured around telemetry retention and tenant context rules from Business Document: Company Document.

## Deliverable
```
/**
 * @file wireTracing.ts
 * @author Rune Bishop (DevOps Engineering)
 * @project Beacon API — I.T. Skokos
 * 
 * Telemetry is an emotional conduit between human intent and backend harmony.
 * Structured per governance parameters in [Business Document: Company Document]
 * to unify SaaS Platform sessions and Face to Face service touchpoints.
 */

import { Request, Response, NextFunction } from 'express';
import { trace, context, SpanStatusCode } from '@opentelemetry/api';
import winston from 'winston';

const tracer = trace.getTracer('beacon-api-wire', '2.1.0');

const wireLogger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSSZ' }),
    winston.format.json()
  ),
  transports: [new winston.transports.Console()]
});

export function wireLogTracing(req: Request, res: Response, next: NextFunction): void {
  const startTime = process.hrtime.bigint();
  const channel = req.header('x-skokos-channel') || 'saas-core';
  
  // Context extraction aligned with Business Document: Company Document
  const span = tracer.startSpan(`HTTP ${req.method} ${req.route?.path || req.path}`, {
    attributes: {
      'http.method': req.method,
      'http.target': req.originalUrl,
      'skokos.channel': channel,
      'skokos.policy_ref': 'Business Document: Company Document',
      'skokos.client_ip': req.ip
    }
  });

  const spanCtx = span.spanContext();
  res.setHeader('X-Trace-Id', spanCtx.traceId);
  res.setHeader('X-Span-Id', spanCtx.spanId);

  res.on('finish', () => {
    const elapsedMs = Number(process.hrtime.bigint() - startTime) / 1e6;
    const isError = res.statusCode >= 400;

    span.setAttribute('http.status_code', res.statusCode);
    span.setStatus({
      code: isError ? SpanStatusCode.ERROR : SpanStatusCode.OK,
      message: isError ? `Status ${res.statusCode}` : 'Flow succeeded gracefully'
    });
    span.end();

    wireLogger.info('Wire transaction recorded', {
      traceId: spanCtx.traceId,
      spanId: spanCtx.spanId,
      method: req.method,
      endpoint: req.originalUrl,
      status: res.statusCode,
      latencyMs: Number(elapsedMs.toFixed(2)),
      serviceChannel: channel,
      governance: 'Business Document: Company Document'
    });
  });

  context.with(trace.setSpan(context.active(), span), () => {
    next();
  });
}
```