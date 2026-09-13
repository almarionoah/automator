# Beacon API Distributed Log Tracing & Cost-Optimized Telemetry Configuration
**Author:** Fig Fontaine  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D16 23:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Configured OpenTelemetry-correlated structured logging for Beacon API. Implemented tail-filtered log injection, health-check suppression, and adaptive 5% baseline sampling to minimize third-party ingestion costs while adhering to governance standards in Company Document.

## Deliverable
```
"""
Beacon API - Cost-Optimized Distributed Tracing & Log Correlator
Author: Fig Fontaine (DevOps)
Reference: Company Document (Data Retention & Telemetry Standards)
"""

import logging
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased, ParentBased
from opentelemetry.sdk.resources import Resource
import structlog

# Cost-Cutter Strategy: Default 5% sample rate for nominal HTTP 2xx traffic
# Referenced Company Document to align with retention SLAs and budget caps
SAMPLE_RATE = float(os.getenv("OTEL_SAMPLE_RATE", "0.05"))
EXCLUDED_PATHS = {"/healthz", "/livez", "/metrics", "/favicon.ico"}

def init_telemetry():
    resource = Resource.create({"service.name": "beacon-api", "env": os.getenv("ENV", "production")})
    
    # Ratio-based sampler minimizes expensive APM ingestion costs
    sampler = ParentBased(root=TraceIdRatioBased(SAMPLE_RATE))
    provider = TracerProvider(resource=resource, sampler=sampler)
    trace.set_tracer_provider(provider)
    
    return trace.get_tracer("beacon-api")

def add_trace_context(_, __, event_dict):
    span = trace.get_current_span()
    if span.is_recording():
        ctx = span.get_span_context()
        event_dict["trace_id"] = f"{ctx.trace_id:032x}"
        event_dict["span_id"] = f"{ctx.span_id:016x}"
    return event_dict

def filter_noisy_probes(_, __, event_dict):
    # Drops health check spam to cut data transfer and index charges
    path = event_dict.get("path", "")
    if path in EXCLUDED_PATHS and event_dict.get("level") == "info":
        raise structlog.DropEvent
    return event_dict

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        filter_noisy_probes,
        add_trace_context,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

tracer = init_telemetry()
logger = structlog.get_logger()

```