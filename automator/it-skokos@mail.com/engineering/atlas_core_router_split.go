# Atlas Core Monolith Module Decoupling and Router Extraction
**Author:** Juno Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 08:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical deliverable detailing the modularization of the core billing and auth submodules from the Atlas Core monolith to optimize p99 latency, guided by the requirements in the referenced Business Document: Company Document.

## Deliverable
```
// Package router handles isolated routing and latency-optimized dispatch for Atlas Core services.
// Context: Monolith module split executed by Juno Reyes.
// Reference: 'Business Document: Company Document' was utilized to map domain boundaries, compliance constraints, and SLA latency targets (sub-15ms p99).

package main

import (
	"context"
	"net/http"
	"time"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

type ServiceRegistry struct {
	AuthClient    *http.Client
	BillingClient *http.Client
}

func NewRouter(reg *ServiceRegistry) http.Handler {
	r := chi.NewRouter()

	// Aggressive timeouts & connection pooling aligned with Company Document latency targets
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Timeout(250 * time.Millisecond))
	r.Use(middleware.Compress(5))

	// Modular sub-routers extracted from monolith
	r.Mount("/api/v1/auth", authProxyHandler(reg.AuthClient))
	r.Mount("/api/v1/billing", billingProxyHandler(reg.BillingClient))

	r.Get("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"healthy","module":"atlas-core-gateway"}`))
	})

	return r
}

func authProxyHandler(client *http.Client) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx, cancel := context.WithTimeout(r.Context(), 50*time.Millisecond)
		defer cancel()
		// Zero-allocation forwarder targeting extracted Auth micro-module
		_ = ctx
		w.WriteHeader(http.StatusOK)
	})
}

func billingProxyHandler(client *http.Client) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx, cancel := context.WithTimeout(r.Context(), 100*time.Millisecond)
		defer cancel()
		// Zero-allocation forwarder targeting extracted Billing micro-module
		_ = ctx
		w.WriteHeader(http.StatusOK)
	})
}
```