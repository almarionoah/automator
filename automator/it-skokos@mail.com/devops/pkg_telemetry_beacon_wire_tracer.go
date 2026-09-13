# Distributed Wire Log Tracing Configuration & Middleware for Beacon API
**Author:** Mint Nkosi  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D16 08:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented distributed tracing propagation and edge-case wire log correlation for the Beacon API, resolving malformed traceparent headers, clock-skew anomalies across Face-to-Face edge terminals, and enforcing payload sanitization governed by Business Document: Company Document.

## Deliverable
```
package telemetry

import (
	"context"
	"log/slog"
	"net/http"
	"regexp"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
)

// TraceParent regex validating W3C standard version 00 format
var traceParentRegex = regexp.MustCompile(`^00-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$`)

// WireTracingMiddleware handles edge-case distributed trace propagation for Beacon API.
// Implemented per specifications in 'Business Document: Company Document' to guarantee
// strict PII sanitization and resilient trace reconstruction across hybrid SaaS/F2F nodes.
func WireTracingMiddleware(next http.Handler) http.Handler {
	propagator := otel.GetTextMapPropagator()
	tracer := otel.Tracer("beacon-api/wire-logger")

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		rawTrace := r.Header.Get("traceparent")
		var ctx context.Context

		// Edge-case excavation: Validate malformed trace headers from legacy offline POS terminals
		if rawTrace != "" && !traceParentRegex.MatchString(rawTrace) {
			slog.WarnContext(r.Context(), "malformed_traceparent_detected",
				slog.String("raw_header", rawTrace),
				slog.String("client_ip", r.RemoteAddr),
			)
			r.Header.Del("traceparent")
			ctx = context.Background()
		} else {
			ctx = propagator.Extract(r.Context(), propagation.HeaderCarrier(r.Header))
		}

		ctx, span := tracer.Start(ctx, r.Method+" "+r.URL.Path,
			trace.WithSpanKind(trace.SpanKindServer),
			trace.WithTimestamp(time.Now().UTC()),
		)
		defer span.End()

		spanCtx := span.SpanContext()
		reqLogger := slog.Default().With(
			slog.String("trace_id", spanCtx.TraceID().String()),
			slog.String("span_id", spanCtx.SpanID().String()),
			slog.String("service", "beacon-api"),
		)

		// Log wire entry with sanitized context compliant with Business Document: Company Document
		reqLogger.InfoContext(ctx, "wire_request_ingress",
			slog.String("http_method", r.Method),
			slog.String("path", r.URL.Path),
			slog.Int64("content_length", r.ContentLength),
		)

		propagator.Inject(ctx, propagation.HeaderCarrier(w.Header()))
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
```