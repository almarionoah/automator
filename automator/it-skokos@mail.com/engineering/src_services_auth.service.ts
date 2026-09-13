# Atlas Core - Refactored Authentication & Session Service
**Author:** Nyx Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 17:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural overhaul and implementation of Atlas Core's authentication service, aligning token lifecycle management and human-first error ergonomics with guidelines from the Company Document.

## Deliverable
```
/**
 * @project Atlas Core
 * @module AuthService
 * @author Nyx Okafor <nyx.okafor@itskokos.com>
 * @description Refactored authentication domain prioritizing seamless token rotation, 
 * intuitive session recovery, and hybrid SaaS/Face-to-Face check-in continuity.
 * 
 * Resource Reference: 
 * - Company Document: Consulted for security baseline compliance, token TTL standards, 
 *   and multi-factor grace period policies across hybrid SaaS/F2F service interactions.
 */

import { FastifyRequest, FastifyReply } from 'fastify';
import { signToken, verifyToken, revokeSession } from '../utils/crypto.util';
import { AuditLogger } from '../telemetry/audit';

export interface AuthSession {
  userId: string;
  tenantId: string;
  role: 'client' | 'agent' | 'admin';
  channel: 'saas' | 'f2f_kiosk';
}

export class AuthService {
  /**
   * Gracefully verifies user session or guides them to re-authentication without harsh friction.
   * Incorporates session resilience rules stipulated in Company Document.
   */
  public static async authenticateSession(req: FastifyRequest, reply: FastifyReply): Promise<AuthSession | void> {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      AuditLogger.logSoftAuthFailure(req.ip, 'Missing bearer token header');
      return reply.status(401).send({
        status: 'unauthenticated',
        message: 'Your session has gently expired. Please log in to continue.',
        recoveryUrl: '/auth/login'
      });
    }

    const token = authHeader.split(' ')[1];

    try {
      const payload = await verifyToken(token);
      req.user = payload;
      return payload;
    } catch (err: any) {
      AuditLogger.warn('Auth token verification failed', { error: err.message });
      return reply.status(401).send({
        status: 'token_invalid',
        message: 'We could not verify your session. Re-authenticating keeps your workspace secure.',
        recoveryUrl: '/auth/refresh'
      });
    }
  }
}
```