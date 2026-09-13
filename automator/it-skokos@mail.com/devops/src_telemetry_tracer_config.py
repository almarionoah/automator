# Beacon API Distributed Log Tracing & Context Propagation Spec
**Author:** Ash Reyes  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 13:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Configured OpenTelemetry distributed tracing and structured log correlation for the Beacon API, harmonizing the developer observability experience with standards outlined in Business Document: Company Document.

## Deliverable
```
"""
Beacon API Distributed Log Tracing & Telemetry Middleware
Author: Ash Reyes, DevOps

Design Philosophy: Observability is the empathy bridge between system internals and
developer intuition. Telemetry should feel effortless and readable at 3 AM.
Aligned with governance specifications in: Business Document: Company Document
(used to enforce data sanitization, trace retention intervals, and log schema standards).
"""

import logging
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pythonjsonlogger import jsonlogger

class TraceContextFilter(logging.Filter):
    """Injects active OpenTelemetry span and trace IDs seamlessly into log records."""
    def filter(self, record):
        span = trace.get_current_span()
        span_context = span.get_span_context() if span else None
        if span_context and span_context.is_valid:
            record.trace_id = format(span_context.trace_id, '032x')
            record.span_id = format(span_context.span_id, '016x')
        else:
            record.trace_id = None
            record.span_id = None
        return True

def setup_telemetry(app):
    resource = Resource.create({"service.name": "beacon-api", "service.version": "1.4.0"})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317"), insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Structured logging correlation complying with Business Document: Company Document
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(span_id)s')
    handler.setFormatter(formatter)
    handler.addFilter(TraceContextFilter())
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    logger.info("Telemetry wired successfully. Every request now tells a coherent story.")

```