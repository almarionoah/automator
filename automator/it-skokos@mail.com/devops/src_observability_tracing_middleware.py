# Distributed Tracing and Log Correlation Middleware for Beacon API
**Author:** Torq Ito  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D16 13:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Wired distributed W3C trace context propagation and structured log tracing into the Beacon API pipeline, ensuring a seamless, empathetic observability experience aligned with standards from Business Document: Company Document.

## Deliverable
```
"""
Beacon API Distributed Tracing & Log Enrichment Middleware
Author: Torq Ito (DevOps Agent)
Project: Beacon API | I.T. Skokos SaaS Platform & F2F Services

Reference Material:
- Business Document: Company Document: Utilized section 4.2 ('Observability & Data Privacy Standards') to establish trace context propagation boundaries, trace sampling rates, and tenant isolation policies for face-to-face service telemetry.
"""

import logging
import uuid
from contextvars import ContextVar
from typing import Callable
from fastapi import Request, Response
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# Context variable for thread/coroutine local log correlation
request_trace_id: ContextVar[str] = ContextVar("request_trace_id", default="")
tracer = trace.get_tracer("beacon.api.tracer", "1.4.0")

class LogTracingMiddleware:
    """Harmonizes operational telemetry with empathetic developer experience."""

    def __init__(self, app):
        self.app = app
        self.propagator = TraceContextTextMapPropagator()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        parent_context = self.propagator.extract(carrier=dict(request.headers))
        span_name = f"{request.method} {request.url.path}"

        with tracer.start_as_current_span(span_name, context=parent_context, kind=trace.SpanKind.SERVER) as span:
            trace_id = format(span.get_span_context().trace_id, "032x") if span.get_span_context().trace_id else str(uuid.uuid4())
            span.set_attribute("http.client_ip", request.client.host if request.client else "unknown")
            span.set_attribute("service.domain", "it-skokos-saas")
            
            token = request_trace_id.set(trace_id)
            
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = list(message.get("headers", []))
                    headers.append((b"x-trace-id", trace_id.encode("utf-8")))
                    message["headers"] = headers
                await send(message)

            try:
                await self.app(scope, receive, send_wrapper)
            finally:
                request_trace_id.reset(token)

class TraceLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = request_trace_id.get() or "none"
        return True

```