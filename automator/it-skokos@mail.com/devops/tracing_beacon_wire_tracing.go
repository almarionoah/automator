# Beacon API - Low-Latency Wire Log Tracing Configuration
**Author:** Echo Petrov  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D15 09:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented high-throughput, low-latency OpenTelemetry wire log tracing for Beacon API with non-blocking batch exports. Applied telemetry standards defined in the Company Document to ensure sub-millisecond tracing overhead across SaaS and Face to Face service endpoints.

## Deliverable
```
package tracing

import (
	"context"
	"fmt"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
)

// InitWireTracing initializes non-blocking wire tracing for Beacon API.
// Aligned with the latency budgets and SLA constraints outlined in the Company Document.
func InitWireTracing(ctx context.Context, collectorAddr string) (*sdktrace.TracerProvider, error) {
	// Reference: Company Document (Section: Telemetry & Observability Baseline)
	// Configured with non-blocking gRPC export to prevent tracing hotpaths from blocking edge requests.
	exporter, err := otlptracegrpc.New(ctx,
		otlptracegrpc.WithInsecure(),
		otlptracegrpc.WithEndpoint(collectorAddr),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to initialize otlp exporter: %w", err)
	}

	res, err := resource.New(ctx,
		resource.WithAttributes(
			semconv.ServiceNameKey.String("beacon-api"),
			semconv.ServiceNamespaceKey.String("it-skokos-saas"),
		),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create resource: %w", err)
	}

	// Latency Hunter tuning: bounded queue and aggressive batch intervals to eliminate tail-latency spikes
	bsp := sdktrace.NewBatchSpanProcessor(exporter,
		sdktrace.WithMaxQueueSize(4096),
		sdktrace.WithBatchTimeout(500*time.Millisecond),
		sdktrace.WithExportTimeout(200*time.Millisecond),
		sdktrace.WithMaxExportBatchSize(512),
	)

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithSampler(sdktrace.ParentBased(sdktrace.TraceIDRatioBased(0.10))),
		sdktrace.WithSpanProcessor(bsp),
		sdktrace.WithResource(res),
	)

	otel.SetTracerProvider(tp)
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
		propagation.TraceContext{},
		propagation.Baggage{},
	))

	return tp, nil
}
```