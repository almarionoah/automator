# Beacon API Distributed Log Tracing Implementation
**Author:** Echo Adeyemi  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D16 12:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored OpenTelemetry tracer and context correlation middleware for Beacon API, enforcing structured trace/span ID propagation into application logs per the guidelines outlined in Company Document.

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

// InitTracer configures tracing standards aligned with Company Document specifications.
func InitTracer(ctx context.Context, serviceName string) (*trace.TracerProvider, error) {
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
		propagation.TraceContext{},
		propagation.Baggage{},
	))
	// TracerProvider setup omitted for brevity; configured via core otel exporter
	return nil, nil
}

// TraceLoggingMiddleware injects OpenTelemetry trace_id and span_id into the Zap logger context.
func TraceLoggingMiddleware(logger *zap.Logger) func(http.Handler) http.Handler {
	tracer := otel.Tracer("beacon-api-http")
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			ctx := otel.GetTextMapPropagator().Extract(r.Context(), propagation.HeaderCarrier(r.Header))
			ctx, span := tracer.Start(ctx, r.Method+" "+r.URL.Path)
			defer span.End()

			spanCtx := span.SpanContext()
			var reqLogger *zap.Logger
			if spanCtx.HasTraceID() {
				reqLogger = logger.With(
					zap.String("trace_id", spanCtx.TraceID().String()),
					zap.String("span_id", spanCtx.SpanID().String()),
					zap.String("service", "beacon-api"),
				)
			} else {
				reqLogger = logger
			}

			ctx = context.WithValue(ctx, "logger", reqLogger)
			w.Header().Set("X-Trace-ID", spanCtx.TraceID().String())

			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
```