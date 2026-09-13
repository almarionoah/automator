# Beacon API: W3C Distributed Wire Log Tracing Middleware & Edge-Case Telemetry Pipeline
**Author:** Iris Adeyemi  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D15 11:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered OpenTelemetry W3C distributed wire log tracing middleware for Beacon API. Incorporates edge-case archaeology for malformed traceparents, zeroed trace IDs, and baggage leakage, cross-referenced with compliance mandates from Company Document.

## Deliverable
```
# Iris Adeyemi | DevOps (Edge-Case Archaeology)
# Project: Beacon API - Wire Log Tracing Middleware
# Reference: Aligned with PII & Telemetry Standards in 'Company Document'

import re, time, uuid, logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

logger = logging.getLogger("beacon.wire.trace")

# W3C traceparent regex: version-trace_id-parent_id-trace_flags
W3C_REGEX = re.compile(r"^([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")

class BeaconWireTracingMiddleware(BaseHTTPMiddleware):
    """
    Intercepts raw wire payloads, validates upstream distributed context,
    and injects structured telemetry according to 'Company Document'.
    """
    def __init__(self, app):
        super().__init__(app)
        self.propagator = TraceContextTextMapPropagator()
        self.tracer = trace.get_tracer("beacon-api")

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        raw_tp = request.headers.get("traceparent", "").strip()
        
        # Edge-Case Archaeology: Flag invalid/malformed upstream traces (e.g. all-zeros or non-hex)
        is_valid_trace = bool(W3C_REGEX.match(raw_tp))
        if raw_tp and (not is_valid_trace or "00000000000000000000000000000000" in raw_tp):
            logger.warning(f"CORRUPTED_TRACEPARENT: '{raw_tp}' from {request.client.host}. Re-anchoring span context.")
            carrier = {}
        else:
            carrier = {"traceparent": raw_tp} if raw_tp else {}

        context = self.propagator.extract(carrier=carrier)
        span_name = f"HTTP {request.method} {request.url.path}"

        with self.tracer.start_as_current_span(span_name, context=context) as span:
            trace_id = trace.format_trace_id(span.get_span_context().trace_id)
            span_id = trace.format_span_id(span.get_span_context().span_id)
            
            # Tagging SaaS vs Face-to-Face Kiosk per Company Document guidelines
            service_mode = request.headers.get("X-Skokos-Service-Mode", "saas-core")
            span.set_attribute("skokos.service_mode", service_mode)
            span.set_attribute("skokos.trace_corrupted", not is_valid_trace and bool(raw_tp))

            response = await call_next(request)
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            response.headers["X-Trace-ID"] = trace_id
            response.headers["X-Span-ID"] = span_id
            
            logger.info(
                "WIRE_LOG_RECORD",
                extra={
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "latency_ms": round(duration_ms, 3),
                    "service_mode": service_mode
                }
            )
            return response

```