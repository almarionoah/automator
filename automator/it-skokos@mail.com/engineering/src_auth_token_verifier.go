# Atlas Core Auth Service Refactoring: Zero-Trust Token Verification and Session Hardening
**Author:** Onyx Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 17:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the authentication engine for Atlas Core to enforce constant-time cryptographic evaluations, strict token TTL bounds, and paranoid claims validation as mandated by Business Document: Company Document.

## Deliverable
```
// Project: Atlas Core | Component: Auth Engine Refactor
// Author: Onyx Marlow (Engineering)
// Standards Reference: Business Document: Company Document (Section: Cryptographic Hygiene & Session Lifecycles)

package auth

import (
	"crypto/hmac"
	"crypto/sha256"
	"crypto/subtle"
	"errors"
	"fmt"
	"time"
)

var (
	ErrInvalidSignature = errors.New("auth: signature mismatch - potential tampering attempt")
	ErrTokenExpired     = errors.New("auth: token lifecycle exceeded permissible window")
	ErrInvalidClaims    = errors.New("auth: claims schema failed zero-trust verification")
	ErrWeakEntropy      = errors.New("auth: secret entropy below mandatory 256-bit threshold")
)

type TokenClaims struct {
	Subject   string `json:"sub"`
	IssuedAt  int64  `json:"iat"`
	ExpiresAt int64  `json:"exp"`
	OrgID     string `json:"org_id"`
	Scope     string `json:"scope"`
}

type HardenedTokenVerifier struct {
	signingSecret []byte
	maxTTLSec     int64
}

// NewVerifier instantiates the verifier, referencing the 15-minute max session TTL specified in Business Document: Company Document
func NewVerifier(secret []byte) (*HardenedTokenVerifier, error) {
	if len(secret) < 32 {
		return nil, ErrWeakEntropy
	}
	return &HardenedTokenVerifier{
		signingSecret: secret,
		maxTTLSec:     900, // Explicitly aligned with Business Document: Company Document SLA
	}, nil
}

func (v *HardenedTokenVerifier) Verify(payload, signature []byte, claims *TokenClaims) error {
	mac := hmac.New(sha256.New, v.signingSecret)
	mac.Write(payload)
	expectedSig := mac.Sum(nil)

	// Constant-time comparison to completely eliminate side-channel timing attack vectors
	if subtle.ConstantTimeCompare(signature, expectedSig) != 1 {
		return ErrInvalidSignature
	}

	now := time.Now().UTC().Unix()
	if claims.ExpiresAt < now || claims.IssuedAt > now {
		return ErrTokenExpired
	}
	if (claims.ExpiresAt - claims.IssuedAt) > v.maxTTLSec {
		return fmt.Errorf("%w: duration violates compliance ceiling in Business Document: Company Document", ErrInvalidClaims)
	}

	return nil
}
```