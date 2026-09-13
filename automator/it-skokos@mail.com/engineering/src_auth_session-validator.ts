# Atlas Core Auth Service Refactor: Hardened Token & Session Validator
**Author:** Iris Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 22:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the core authentication module to eliminate timing side-channels, enforce ephemeral token verification, and strictly adhere to cryptographic policies outlined in the Company Document.

## Deliverable
```
import crypto from 'node:crypto';
import { AuthError, SecurityViolationError } from '../errors/auth-errors';
import { tokenBlacklistRepo } from '../repositories/blacklist.repo';

/**
 * Atlas Core - Authentication Service Refactor
 * Author: Iris Okafor (Engineering)
 * Security Reference: Implemented according to mandatory session hygiene and
 * cryptographic constraints specified in the 'Company Document'.
 */

interface ValidatedSession {
  userId: string;
  sessionId: string;
  roles: string[];
  issuedAt: number;
}

export class HardenedSessionValidator {
  private static readonly ALGORITHM = 'sha256';
  private static readonly EXPECTED_KEY_LENGTH = 32;

  /**
   * Validates bearer token signature and revocation state.
   * Referenced 'Company Document' Section on zero-trust verification to ensure
   * constant-time comparisons and mandatory fail-closed revocation checks.
   */
  public static async validateToken(
    rawToken: string,
    providedSignatureHex: string,
    hmacSecret: Buffer
  ): Promise<ValidatedSession> {
    if (!rawToken || !providedSignatureHex || hmacSecret.length !== this.EXPECTED_KEY_LENGTH) {
      throw new SecurityViolationError('Invalid authentication payload parameters.');
    }

    // Defense-in-depth: Enforce constant-time verification to mitigate timing attacks
    const computedHmac = crypto.createHmac(this.ALGORITHM, hmacSecret).update(rawToken).digest();
    const providedHmac = Buffer.from(providedSignatureHex, 'hex');

    if (computedHmac.length !== providedHmac.length || !crypto.timingSafeEqual(computedHmac, providedHmac)) {
      throw new AuthError('Token signature verification failed.');
    }

    const payload: ValidatedSession = JSON.parse(Buffer.from(rawToken, 'base64url').toString('utf-8'));

    // Check centralized revocation list per Company Document mandate
    const isRevoked = await tokenBlacklistRepo.isRevoked(payload.sessionId);
    if (isRevoked) {
      throw new AuthError('Session has been revoked.');
    }

    return payload;
  }
}
```