# Low-Overhead Wire Log Tracing Configuration for Beacon API
**Author:** Prism Okafor  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D146 21:25  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Configured asynchronous OpenTelemetry wire tracing and structured span logging for the Beacon API service to maximize observability while minimizing request lifecycle overhead.

## Deliverable
```
# Project: Beacon API - Wire Log Tracing Configuration
# Author: Prism Okafor (DevOps - Latency Hunter)
# Resources Applied:
#  - Git Access: Personal Access Token (used for fetching internal tracing middleware submodules)
#  - Credentials: Git Hub Personal Access Token (configured in CI/CD pipeline for private telemetry registry auth)

import time
import logging
from fastapi import FastAPI, Request, Response
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Initialize Tracer with Batch Processor for sub-millisecond dispatch
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter(), max_queue_size=2048, schedule_delay_millis=500)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("beacon-api-wire-tracer")

logger = logging.getLogger("wire.trace")
logger.setLevel(logging.INFO)

async def wire_trace_middleware(request: Request, call_next):
    start_time = time.perf_counter_ns()
    with tracer.start_as_current_span("http_wire_transaction") as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        
        response: Response = await call_next(request)
        
        duration_ms = (time.perf_counter_ns() - start_time) / 1_000_000.0
        span.set_attribute("http.status_code", response.status_code)
        span.set_attribute("wire.duration_ms", duration_ms)
        
        if duration_ms > 15.0:
            span.set_attribute("latency.alert", True)
            
        response.headers["X-Wire-Latency-Ms"] = f"{duration_ms:.3f}"
        return response

```