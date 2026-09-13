# Beacon API Distributed Log Tracing Wire & Telemetry Configuration
**Author:** Ash Okafor  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D16 08:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of OpenTelemetry tracing pipeline with W3C trace context propagation and structured JSON log correlation for Beacon API, designed in strict accordance with observability schemas established in Company Document.

## Deliverable
```
"""
Beacon API - Distributed Tracing & Structured Log Correlation Engine
Author: Ash Okafor, DevOps (Data Purist)
Reference: Company Document (Telemetry Data Schemas & Logging Specifications)
"""

import json
import logging
import sys
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# Telemetry metadata configured strictly according to Company Document Section 3.2 (Service Identifiers)
RESOURCE_ATTRIBUTES = {
    "service.name": "beacon-api",
    "service.namespace": "it-skokos-platform",
    "service.version": "2.4.1",
    "service.instance.id": "beacon-prod-eu1-node04",
    "telemetry.sdk.language": "python",
}

def initialize_tracing() -> trace.Tracer:
    resource = Resource.create(RESOURCE_ATTRIBUTES)
    provider = TracerProvider(resource=resource)
    
    exporter = OTLPSpanExporter(endpoint="otel-collector.internal.skokos:4317", insecure=False)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer("beacon.api.tracer", "2.4.1")

class TraceCorrelatedJSONFormatter(logging.Formatter):
    """Strict JSON formatter adhering to the log schema mandated in Company Document."""
    def format(self, record: logging.LogRecord) -> str:
        span = trace.get_current_span()
        ctx = span.get_span_context() if span else None
        
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "severity": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": format(ctx.trace_id, "032x") if ctx and ctx.is_valid else None,
            "span_id": format(ctx.span_id, "016x") if ctx and ctx.is_valid else None,
            "trace_sampled": ctx.trace_flags.sampled if ctx and ctx.is_valid else False,
            "data": getattr(record, "extra_data", {})
        }
        return json.dumps(payload, separators=(",", ":"))

def wire_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(TraceCorrelatedJSONFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [handler]

# Initialize trace context wiring
tracer = initialize_tracing()
wire_logging()

```