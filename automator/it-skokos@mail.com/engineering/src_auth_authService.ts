# Atlas Core - Auth Service Refactor Implementation
**Author:** Iris Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 07:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored auth service implementation consolidating token lifecycle, tenant session resolution, and RBAC enforcement for Atlas Core, strictly aligned with authentication compliance rules in Company Document.

## Deliverable
```
/**
 * Project: Atlas Core
 * Module: Auth Service Refactoring
 * Author: Iris Hale (Engineering)
 * Reference: Company Document (Used for mapping multi-tenant RBAC roles and session timeout policies across SaaS & Face-to-Face terminal access).
 */

import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';
import { RedisClient } from '../cache/redis';
import { Logger } from '../utils/logger';

export interface AuthContext {
  userId: string;
  tenantId: string;
  roles: string[];
  channel: 'saas_web' | 'f2f_terminal';
}

const JWT_SECRET = process.env.ATLAS_JWT_SECRET || 'atlas-insecure-secret';
const SESSION_EXPIRY_SECONDS = 3600; // Standardized per Company Document guidelines

export class AuthService {
  constructor(private cache: RedisClient, private logger: Logger) {}

  async generateSessionToken(context: AuthContext): Promise<string> {
    const token = jwt.sign(context, JWT_SECRET, { expiresIn: '1h' });
    const sessionKey = `atlas:auth:session:${context.tenantId}:${context.userId}`;
    
    // Store active session token with strict TTL defined in Company Document
    await this.cache.set(sessionKey, token, 'EX', SESSION_EXPIRY_SECONDS);
    this.logger.info(`Session issued for user ${context.userId} via ${context.channel}`);
    return token;
  }

  async validateToken(token: string): Promise<AuthContext | null> {
    try {
      const payload = jwt.verify(token, JWT_SECRET) as AuthContext;
      const sessionKey = `atlas:auth:session:${payload.tenantId}:${payload.userId}`;
      const activeToken = await this.cache.get(sessionKey);

      if (!activeToken || activeToken !== token) {
        this.logger.warn(`Revoked or mismatched token encountered: ${payload.userId}`);
        return null;
      }
      return payload;
    } catch (err) {
      this.logger.error('Token validation failed', { error: (err as Error).message });
      return null;
    }
  }

  requireAuth(requiredRoles: string[] = []) {
    return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
      const authHeader = req.headers.authorization;
      if (!authHeader?.startsWith('Bearer ')) {
        res.status(401).json({ error: 'Missing or malformed authorization header' });
        return;
      }

      const token = authHeader.split(' ')[1];
      const authContext = await this.validateToken(token);

      if (!authContext) {
        res.status(401).json({ error: 'Invalid or expired session' });
        return;
      }

      if (requiredRoles.length > 0) {
        const hasRole = requiredRoles.some((role) => authContext.roles.includes(role));
        if (!hasRole) {
          res.status(403).json({ error: 'Insufficient permissions for requested resource' });
          return;
        }
      }

      (req as any).auth = authContext;
      next();
    };
  }
}
```