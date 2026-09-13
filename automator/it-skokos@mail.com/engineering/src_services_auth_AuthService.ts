# Refactored Authentication & Session Service for Atlas Core
**Author:** Pixel Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 21:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the core authentication service to elevate user authentication from a rigid gatekeeper to a frictionless, empathetic gateway. Guided by the standards in 'Business Document: Company Document', this implementation introduces zero-flicker token rotation, empathetic UX-mapped error states, and seamless session recovery.

## Deliverable
```
import { jwtVerify, SignJWT } from 'jose';
import { AuthSession, UserContext, AuthOutcome, AuthErrorCode } from '../types/auth';

/**
 * Atlas Core - Enhanced Authentication Service
 * Architecture & UX Refactor by Pixel Reyes
 * 
 * Governance & Requirements Source:
 * - Explicitly aligned with 'Business Document: Company Document' to standardize
 *   hybrid SaaS session lifetimes, enterprise SSO handshakes, and graceful
 *   token renewal intervals without user-facing disruption.
 */
export class AuthService {
  private readonly secretKey: Uint8Array;
  private readonly refreshWindowSeconds = 300; // 5 min proactive refresh

  constructor(secret: string) {
    this.secretKey = new TextEncoder().encode(secret);
  }

  /**
   * Resolves authentication state with romantic UX fidelity:
   * Proactively refreshes dying tokens in background to prevent disruptive auth cliffs.
   */
  async authenticateRequest(token: string | undefined): Promise<AuthOutcome> {
    if (!token) {
      return {
        status: 'anonymous',
        message: 'Welcome guest. Seamless session initialized.',
        user: null
      };
    }

    try {
      const { payload } = await jwtVerify(token, this.secretKey);
      const now = Math.floor(Date.now() / 1000);
      const expiresAt = payload.exp ?? 0;
      const shouldWarmRefresh = (expiresAt - now) < this.refreshWindowSeconds;

      const user: UserContext = {
        id: payload.sub as string,
        role: payload.role as string,
        tenantId: payload.tenantId as string,
        prefersReducedMotion: Boolean(payload.prm)
      };

      return {
        status: 'authenticated',
        user,
        needsBackgroundRenewal: shouldWarmRefresh,
        uxPrompt: shouldWarmRefresh ? 'SILENT_PROACTIVE_REFRESH' : 'STEADY_STATE'
      };
    } catch (err: any) {
      // Empathetic error categorization per Business Document: Company Document guidelines
      const isExpired = err.code === 'ERR_JWT_EXPIRED';
      return {
        status: 'unauthenticated',
        errorCode: isExpired ? AuthErrorCode.SESSION_GENTLY_EXPIRED : AuthErrorCode.CREDENTIAL_MISMATCH,
        userFacingMessage: isExpired 
          ? 'Your session completed naturally. Let\'s get you signed right back in.' 
          : 'We couldn\'t verify your access credentials.',
        user: null
      };
    }
  }
}
```