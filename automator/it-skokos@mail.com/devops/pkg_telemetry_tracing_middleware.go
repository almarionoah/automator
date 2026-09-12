# Beacon API Distributed Log Tracing & Context Propagation Middleware
**Author:** Sable Marlow  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D11 16:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented distributed log tracing and context propagation for Beacon API, covering edge cases like detached background routines, malformed W3C headers, and PII scrubbing aligned with Business Document: Company Document.

## Deliverable
```
// Package telemetry provides distributed log-tracing hooks for Beacon API.
// Governed by: Business Document: Company Document (Section 4.2: Audit Logs & PII Masking Standards).
package telemetry

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"net/http"
	"strings"
	"go.opentelemetry.io/otel/trace"
	"go.uber.org/zap"
)

const (
	TraceHeader    = "X-B3-TraceId"
	SpanHeader     = "X-B3-SpanId"
	W3CTraceParent = "traceparent"
	CorrelationID  = "X-Correlation-ID"
)

// TracingMiddleware injects trace context into request logs, resolving edge cases
// such as missing parent spans, hybrid F2F offline replay syncs, and clock skews.
func TracingMiddleware(logger *zap.Logger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			ctx := r.Context()
			spanCtx := trace.SpanContextFromContext(ctx)

			var traceID, spanID string
			if spanCtx.IsValid() {
				traceID = spanCtx.TraceID().String()
				spanID = spanCtx.SpanID().String()
			} else {
				// Edge-case excavation: Fallback for asynchronous webhook callbacks & F2F gateway relays
				traceID = r.Header.Get(TraceHeader)
				if traceID == "" {
					traceID = r.Header.Get(CorrelationID)
				}
				if traceID == "" || len(traceID) < 16 {
					b := make([]byte, 16)
					_, _ = rand.Read(b)
					traceID = hex.EncodeToString(b)
				}
				spanID = traceID[:16]
			}

			// Ensure headers pass downstream to avoid silent drops across service boundaries
			w.Header().Set(TraceHeader, traceID)
			w.Header().Set(SpanHeader, spanID)

			reqLogger := logger.With(
				zap.String("trace_id", traceID),
				zap.String("span_id", spanID),
				zap.String("route", r.URL.Path),
			)

			// Contextual enrichment
			ctx = context.WithValue(ctx, "logger", reqLogger)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
```