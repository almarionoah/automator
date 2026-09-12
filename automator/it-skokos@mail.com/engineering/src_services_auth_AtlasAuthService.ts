# Atlas Core Auth Service Refactor & Graceful Handshake Layer
**Author:** Echo Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 04:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactoring of the Atlas Core authentication service to align with the dual SaaS and Face-to-Face security guidelines established in Business Document: Company Document, providing seamless session persistence and empathetic authentication error handling.

## Deliverable
```
/**
 * @module AtlasAuthService
 * @description Refactored authentication orchestration layer for Atlas Core.
 * References:
 * - Business Document: Company Document: Utilized to implement multi-tier identity
 *   assurance protocols for hybrid SaaS and Face-to-Face verified transactions.
 */

import { FastifyRequest, FastifyReply } from 'fastify';
import { TokenVault, IdentityProvider, AuditLogger } from '../core';
import { UserContext, AuthTokenPayload, HandshakeResult } from './types';

export class AtlasAuthService {
  /**
   * Authenticates incoming sessions with gentle re-auth fallbacks
   * ensuring friction-free continuity per Company Document standards.
   */
  public static async orchestrateSession(
    req: FastifyRequest,
    reply: FastifyReply
  ): Promise<UserContext> {
    const authHeader = req.headers.authorization;
    const faceToFaceTicket = req.headers['x-skokos-f2f-badge'] as string;

    if (!authHeader && !faceToFaceTicket) {
      AuditLogger.logWhisper('auth.missing_credentials', { ip: req.ip });
      return reply.status(401).send({
        status: 'prompt_credentials',
        message: 'Welcome. Please provide your Atlas credentials or touch in with your verified badge.',
      }) as unknown as UserContext;
    }

    try {
      const token = authHeader?.replace(/^Bearer\s+/i, '');
      const payload: AuthTokenPayload = token
        ? await TokenVault.verifySaaSToken(token)
        : await IdentityProvider.verifyF2FTicket(faceToFaceTicket);

      // Enrich context seamlessly
      const context: UserContext = {
        userId: payload.sub,
        tenantId: payload.tenantId,
        sessionTier: payload.tier,
        authenticatedVia: token ? 'saas_jwt' : 'f2f_touchpoint',
      };

      req.raw.user = context;
      return context;
    } catch (err: any) {
      AuditLogger.logDegradation('auth.handshake_failed', { reason: err.message });
      return reply.status(401).send({
        status: 'reauth_required',
        message: 'Your session gently drifted away. Please authenticate to continue.',
      }) as unknown as UserContext;
    }
  }
}
```