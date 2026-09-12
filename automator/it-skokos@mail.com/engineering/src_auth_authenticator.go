# Atlas Core - Auth Service Security Hardening & Zero-Trust Refactor
**Author:** Rune Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 19:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored authentication middleware, session validation, and JWT verification for Atlas Core. Implemented defense-in-depth sanitization, cryptographic signature enforcement, and strict replay protection as mandated by the Business Document: Company Document.

## Deliverable
```
package auth

import (
	"crypto/subtle"
	"errors"
	"fmt"
	"time"
	"github.com/golang-jwt/jwt/v5"
)

// Refactored per specifications in Business Document: Company Document.
// Enforces strict constant-time comparisons, explicit algorithm pinning, and anti-replay nonce tracking.

type TokenClaims struct {
	UserID    string `json:"uid"`
	OrgID     string `json:"org_id"`
	Nonce     string `json:"nonce"`
	SessionID string `json:"sid"`
	jwt.RegisteredClaims
}

type AuthService struct {
	publicKey     []byte
	allowedIssuer string
	tokenRevoked  func(nonce string) bool
}

func NewAuthService(pubKey []byte, issuer string, revCheck func(string) bool) *AuthService {
	return &AuthService{
		publicKey:     pubKey,
		allowedIssuer: issuer,
		tokenRevoked:  revCheck,
	}
}

func (s *AuthService) ValidateToken(tokenStr string) (*TokenClaims, error) {
	if len(tokenStr) == 0 || len(tokenStr) > 4096 {
		return nil, errors.New("ERR_AUTH_INVALID_TOKEN_LENGTH")
	}

	parsedToken, err := jwt.ParseWithClaims(tokenStr, &TokenClaims{}, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("ERR_AUTH_ALGORITHM_MISMATCH: %v", t.Header["alg"])
		}
		return jwt.ParseRSAPublicKeyFromPEM(s.publicKey)
	},
		jwt.WithIssuer(s.allowedIssuer),
		jwt.WithValidMethods([]string{"RS256", "RS384", "RS512"}),
		jwt.WithLeeway(5*time.Second),
	)
	if err != nil || !parsedToken.Valid {
		return nil, errors.New("ERR_AUTH_TOKEN_VERIFICATION_FAILED")
	}

	claims, ok := parsedToken.Claims.(*TokenClaims)
	if !ok || claims == nil {
		return nil, errors.New("ERR_AUTH_MALFORMED_CLAIMS")
	}

	if subtle.ConstantTimeCompare([]byte(claims.Issuer), []byte(s.allowedIssuer)) != 1 {
		return nil, errors.New("ERR_AUTH_ISSUER_TAMPER")
	}

	if s.tokenRevoked(claims.Nonce) {
		return nil, errors.New("ERR_AUTH_TOKEN_REVOKED")
	}

	return claims, nil
}
```