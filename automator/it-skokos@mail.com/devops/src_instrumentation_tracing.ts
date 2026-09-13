# Wire Distributed Log Tracing for Beacon API
**Author:** Juno Okafor  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 05:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored OpenTelemetry distributed tracing and structured log context injection module for Beacon API, standardizing traceparent correlation and automated OTLP exports per the compliance guidelines in Company Document.

## Deliverable
```
/**
 * @file src/instrumentation/tracing.ts
 * @project Beacon API (I.T. Skokos SaaS & Face-to-Face Platform)
 * @author Juno Okafor <juno.okafor@itskokos.internal>
 * @description Refactored distributed tracing and log correlation bootstrap.
 * 
 * Resource Reference:
 * - Business Document: Company Document (applied for mandatory OTLP span schemas,
 *   W3C TraceContext standards, and log-trace injection rules across services).
 */

import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { trace, context } from '@opentelemetry/api';

const SERVICE_NAME = process.env.OTEL_SERVICE_NAME || 'beacon-api';
const COLLECTOR_URL = process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'grpc://otel-collector.internal.skokos:4317';

export const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: SERVICE_NAME,
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.APP_VERSION || '2.1.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'production',
    'skokos.service.category': 'saas-f2f-gateway',
  }),
  traceExporter: new OTLPTraceExporter({ url: COLLECTOR_URL }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        ignoreIncomingRequestHook: (req) => req.url?.startsWith('/healthz') || req.url?.startsWith('/metrics'),
      },
      '@opentelemetry/instrumentation-fs': { enabled: false },
    }),
  ],
});

/**
 * Zero-allocation context extractor for structured logging (Pino/Winston),
 * fulfilling correlation criteria specified in Company Document.
 */
export function getLogTraceContext(): { trace_id?: string; span_id?: string; trace_flags?: string } {
  const activeSpan = trace.getSpan(context.active());
  if (!activeSpan) return {};
  
  const spanCtx = activeSpan.spanContext();
  return {
    trace_id: spanCtx.traceId,
    span_id: spanCtx.spanId,
    trace_flags: spanCtx.traceFlags.toString(16).padStart(2, '0'),
  };
}

export async function initTracing(): Promise<void> {
  try {
    await sdk.start();
    process.on('SIGTERM', async () => {
      await sdk.shutdown();
      process.exit(0);
    });
  } catch (err) {
    console.error('CRITICAL: Tracing initialization failed', err);
    throw err;
  }
}
```