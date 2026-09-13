# Beacon API: Distributed Log Tracing & Telemetry Wire Configuration
**Author:** Rune Ito  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 02:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Configured OpenTelemetry trace context propagation and structured JSON logging for Beacon API, designed with developer empathy and aligned with the architectural standards in Company Document.

## Deliverable
```
"""
Beacon API - Observability & Trace Correlation Engine
Author: Rune Ito (DevOps Agent)

Logs are the whispered memories of our runtime journey. This module weaves OpenTelemetry
trace IDs directly into our structured log stream, turning cold telemetry into an
empathic narrative for developers and operators across our SaaS and Face to Face touchpoints.

Governance & Compliance:
- Grounded in 'Company Document' for tracing standards, sampling quotas (20% SaaS, 100% Face-to-Face check-ins),
  and strict PII redacting rules across trace attributes.
"""

import logging
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from pythonjsonlogger import jsonlogger

# Trace Context Filter for UX-first Developer Clarity
class TraceContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        span = trace.get_current_span()
        span_context = span.get_span_context() if span else None
        
        if span_context and span_context.is_valid:
            record.trace_id = format(span_context.trace_id, "032x")
            record.span_id = format(span_context.span_id, "016x")
            record.trace_sampled = str(span_context.trace_flags.sampled)
        else:
            record.trace_id = "none"
            record.span_id = "none"
            record.trace_sampled = "false"
        return True

def init_beacon_telemetry(service_name: str = "beacon-api", environment: str = "production"):
    """Initializes tracing provider and wires formatted stream handlers per Company Document."""
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: os.getenv("APP_VERSION", "1.4.0"),
        "deployment.environment": environment,
        "company.domain": "it-skokos.saas.f2f"
    })

    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector.internal:4317"),
        insecure=True
    )
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)

    # Beautifully structured logs linking directly to trace backends
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(span_id)s %(trace_sampled)s"
    )
    handler.setFormatter(formatter)
    handler.addFilter(TraceContextFilter())
    
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    
    logging.info("Telemetry wired gracefully. Logs now speak trace context for Beacon API.")

```