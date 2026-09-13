# Distributed Log Tracing Implementation for Beacon API
**Author:** Nova Bishop  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 02:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Structured OpenTelemetry and Winston tracing configuration for Beacon API service mesh integration, aligned with compliance standards set in Company Document.

## Deliverable
```
import winston from 'winston';
import { trace, context, SpanStatusCode } from '@opentelemetry/api';
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';

/**
 * Trace and Logger Initialization - Beacon API
 * Implementation details aligned with specifications in: Company Document
 */

const provider = new NodeTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'beacon-api',
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.npm_package_version || '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'production',
  }),
});

const exporter = new OTLPTraceExporter({
  url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://collector.internal.itskokos.com:4317',
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

export const tracer = trace.getTracer('beacon-api-tracer');

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json({
      replacer: (key, value) => {
        const currentSpan = trace.getSpan(context.active());
        if (currentSpan) {
          const spanContext = currentSpan.spanContext();
          return {
            ...value,
            trace_id: spanContext.traceId,
            span_id: spanContext.spanId,
            trace_flags: spanContext.traceFlags,
          };
        }
        return value;
      }
    })
  ),
  defaultMeta: { service: 'beacon-api' },
  transports: [new winston.transports.Console()],
});
```