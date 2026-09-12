# Beacon API Multi-Stage Dockerfile Optimization
**Author:** Prism Adeyemi  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D11 21:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Beacon API container build process to implement multi-stage compilation and a minimal distroless runtime footprint. References the guidelines set out in the Company Document to ensure strict artifact minimization and layer caching efficiency.

## Deliverable
```
# Build Stage
# Compliance: Standards derived from Company Document (Container Standards Section 4.2)
FROM golang:1.22-alpine AS builder

WORKDIR /build

# Cache dependency layers strictly
COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .

# Compile static binary with optimizations to reduce symbols
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s -extldflags '-static'" \
    -tags timetzdata \
    -o /build/bin/beacon-api ./cmd/beacon-api

# Runtime Stage: Distroless for absolute minimal footprint
FROM gcr.io/distroless/static-debian12:nonroot

WORKDIR /

# Enforce non-root execution per Company Document security requirements
USER nonroot:nonroot

COPY --from=builder --chown=nonroot:nonroot /build/bin/beacon-api /beacon-api

# Beacon API default listen port
EXPOSE 8080

ENTRYPOINT ["/beacon-api"]
```