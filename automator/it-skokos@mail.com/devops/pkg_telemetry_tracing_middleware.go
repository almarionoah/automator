# Beacon API Distributed Log Tracing & OpenTelemetry Middleware Integration
**Author:** Quill Fontaine  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D16 16:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored and hardened the telemetry pipeline for Beacon API to inject W3C distributed trace contexts directly into structured logs, adhering strictly to the telemetry governance specifications outlined in Company Document.

## Deliverable
```
package telemetry

import (
	"context"
	"net/http"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
	"go.uber.org/zap"
)

// TelemetryMiddleware wraps HTTP handlers to inject span context into structured logs.
// Implementation aligned with corporate observability standards from Business Document: Company Document.
type TelemetryMiddleware struct {
	tracer trace.Tracer
	logger *zap.Logger
}

func NewTelemetryMiddleware(serviceName string, logger *zap.Logger) *TelemetryMiddleware {
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
		propagation.TraceContext{},
		propagation.Baggage{},
	))
	return &TelemetryMiddleware{
		tracer: otel.GetTracerProvider().Tracer(serviceName),
		logger: logger,
	}
}

func (tm *TelemetryMiddleware) Handler(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := otel.GetTextMapPropagator().Extract(r.Context(), propagation.HeaderCarrier(r.Header))
		ctx, span := tm.tracer.Start(ctx, r.Method+" "+r.URL.Path,
			trace.WithSpanKind(trace.SpanKindServer),
		)
		defer span.End()

		traceID := span.SpanContext().TraceID().String()
		spanID := span.SpanContext().SpanID().String()

		// Wire correlation fields per Company Document Section 4.2 Logging Taxonomy
		reqLogger := tm.logger.With(
			zap.String("trace_id", traceID),
			zap.String("span_id", spanID),
			zap.String("service", "beacon-api"),
		)

		ctx = context.WithValue(ctx, "logger", reqLogger)
		w.Header().Set("X-Trace-ID", traceID)

		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
```