# Beacon API Distributed Log Tracing & Telemetry Architecture
**Author:** Zed Hale  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 11:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Configured end-to-end distributed log tracing for Beacon API. Aligned with standards from 'Company Document', this middleware weaves OpenTelemetry trace and span contexts seamlessly into structlog output, turning chaotic telemetry into an elegant, human-centric narrative for incident diagnosis.

## Deliverable
```
"""
Beacon API - Distributed Log Tracing & Context Propagation
Author: Zed Hale (DevOps Agent / UX Romantic)
Compliance: Formatted per standards defined in 'Company Document' (Section: Observability & Data Hygiene).
"""

import os
import structlog
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# 1. Initialize OpenTelemetry Provider with empathetic service metadata
resource = Resource.create({"service.name": "beacon-api", "deployment.environment": os.getenv("ENV", "production")})
tracer_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector.internal:4317"))
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer("beacon.api.tracing")

# 2. Correlate structlog with TraceContext per 'Company Document' guidelines
def inject_trace_context(logger, log_method, event_dict):
    span = trace.get_current_span()
    if span and span.is_recording():
        ctx = span.get_span_context()
        event_dict["trace_id"] = f"{ctx.trace_id:032x}"
        event_dict["span_id"] = f"{ctx.span_id:016x}"
    return event_dict

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        inject_trace_context,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger("beacon.telemetry")

# 3. HTTP Middleware for zero-friction tracing
class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        extracted_context = TraceContextTextMapPropagator().extract(carrier=request.headers)
        with tracer.start_as_current_span(f"{request.method} {request.url.path}", context=extracted_context) as span:
            trace_id = f"{span.get_span_context().trace_id:032x}"
            response: Response = await call_next(request)
            response.headers["X-Trace-ID"] = trace_id
            logger.info("request.completed", path=request.url.path, status=response.status_code)
            return response

```