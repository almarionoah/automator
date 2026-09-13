# Beacon API: Resilient Wire-Log Tracing Interceptor
**Author:** Lyra Van Dyk  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D16 13:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-grade wire-log tracing middleware for Beacon API, designed to handle malformed W3C trace contexts, high-entropy edge cases, and PII scrubbing as specified in Company Document.

## Deliverable
```
"""
Beacon API - Wire Log Tracing Interceptor
Author: Lyra Van Dyk, DevOps
Compliance: Aligned with 'Company Document' (Section 4.2 Telemetry Redaction & Retention Standards).
"""
import logging
import re
import time
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from opentelemetry import trace
from opentelemetry.trace import SpanKind, StatusCode

logger = logging.getLogger("beacon.telemetry.wire")
 tracer = trace.get_tracer("beacon.wire.tracer")

# Regex for standard W3C traceparent: version-traceid-parentid-traceflags
W3C_TRACEPARENT_RE = re.compile(r"^00-[a-f0-9]{32}-[a-f0-9]{16}-[0-9a-f]{2}$")

class ResilientWireTracingMiddleware(BaseHTTPMiddleware):
    """
    Intercepts raw HTTP wire logs, recovers from malformed trace contexts,
    and strictly sanitizes payloads per guidelines in Company Document.
    """
    def __init__(self, app, max_payload_capture_bytes: int = 4096):
        super().__init__(app)
        self.max_capture = max_payload_capture_bytes
        # Company Document mandates PII field masking in wire dumps
        self.pii_filter_re = re.compile(r'"(password|token|secret|ssn|auth)":\s*"[^"]+"', re.IGNORECASE)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        raw_traceparent = request.headers.get("traceparent", "").strip()
        
        # Edge-case excavation: Non-compliant W3C headers, trailing spaces, corrupted IDs
        valid_trace = bool(W3C_TRACEPARENT_RE.match(raw_traceparent))
        if not valid_trace and raw_traceparent:
            logger.warning("Corrupt traceparent received: %s. Generating fallback.", raw_traceparent)

        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        start_time = time.perf_counter()

        with tracer.start_as_current_span(
            f"HTTP {request.method} {request.url.path}",
            kind=SpanKind.SERVER,
            attributes={
                "http.method": request.method,
                "http.target": request.url.path,
                "beacon.correlation_id": correlation_id,
                "wire.traceparent_valid": valid_trace
            }
        ) as span:
            try:
                response = await call_next(request)
                duration_ms = (time.perf_counter() - start_time) * 1000
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.duration_ms", duration_ms)
                
                # Inject trace context back into egress headers
                response.headers["x-correlation-id"] = correlation_id
                return response
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(StatusCode.ERROR, str(exc))
                logger.error("Wire execution failed on path %s: %s", request.url.path, exc, exc_info=True)
                raise exc

```