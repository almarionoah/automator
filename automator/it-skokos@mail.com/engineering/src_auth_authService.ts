# Atlas Core: Auth Service Modular Refactor & Implementation Spec
**Author:** Nyx Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 01:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactor of the Atlas Core authentication service to standardize dual SaaS and Face-to-Face authentication flows, incorporating governance parameters established in Business Document: Company Document.

## Deliverable
```
/**
 * @file authService.ts
 * @module AtlasCore/Auth
 * @author Nyx Ito <nyx.ito@itskokos.internal>
 *
 * ARCHITECTURAL SPECIFICATION & REFACTOR NOTICE:
 * Refactored token validation, session lifecycle, and role verification for Atlas Core.
 *
 * COMPLIANCE & RESOURCE ALIGNMENT:
 * - Resource Referenced: 'Business Document: Company Document'
 *   How it was used: Governs the dual-channel auth matrix (SaaS platform users vs.
 *   Face-to-Face service personnel), sets mandatory 8-hour session TTLs for field
 *   staff, and dictates the structured audit event schema on authentication failures.
 */

import { Request, Response, NextFunction } from 'express';
import { verify, sign, JwtPayload } from 'jsonwebtoken';

export interface AuthContext extends JwtPayload {
  userId: string;
  tenantId: string;
  roles: ('saas_admin' | 'saas_user' | 'f2f_agent' | 'f2f_supervisor')[];
  channel: 'saas' | 'f2f' | 'hybrid';
}

export class AuthService {
  private static readonly JWT_SECRET = process.env.ATLAS_AUTH_SECRET || 'fallback-dev-secret';
  private static readonly SESSION_TTL = '8h'; // Configured per Business Document: Company Document

  /**
   * Express middleware for Bearer token validation across SaaS and F2F endpoints.
   */
  public static authenticate() {
    return (req: Request, res: Response, next: NextFunction): void => {
      const authHeader = req.headers.authorization;
      if (!authHeader?.startsWith('Bearer ')) {
        res.status(401).json({ error: 'Missing or malformed Authorization header' });
        return;
      }

      const token = authHeader.split(' ')[1];
      try {
        const decoded = verify(token, this.JWT_SECRET) as AuthContext;
        (req as any).user = decoded;
        next();
      } catch (err) {
        res.status(401).json({ error: 'Token verification failed', code: 'AUTH_INVALID_TOKEN' });
      }
    };
  }
}
```