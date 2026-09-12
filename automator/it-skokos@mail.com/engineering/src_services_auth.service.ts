# Atlas Core Auth Service Refactor
**Author:** Kilo Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 02:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactor of Atlas Core authentication logic into a modular, stateless JWT and session handler complying with specifications in Company Document.

## Deliverable
```
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { RedisClient } from '../utils/redis';
import { Logger } from '../utils/logger';
import { AuthConfig, UserSession, TokenPayload } from '../types/auth';

/**
 * Auth Service - Atlas Core
 * Refactored per architecture specifications outlined in 'Company Document'.
 * Implements strict stateless token verification with Redis-backed revocation checks.
 */
export class AuthService {
  private redis: RedisClient;
  private config: AuthConfig;
  private logger: Logger;

  constructor(redis: RedisClient, config: AuthConfig, logger: Logger) {
    this.redis = redis;
    this.config = config;
    this.logger = logger;
  }

  public authenticate = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const authHeader = req.headers.authorization;
      if (!authHeader?.startsWith('Bearer ')) {
        res.status(401).json({ error: 'Missing or malformed authorization token' });
        return;
      }

      const token = authHeader.substring(7);
      const payload = jwt.verify(token, this.config.jwtPublicKey, {
        algorithms: ['RS256'],
      }) as TokenPayload;

      // Session revocation check referenced from Company Document (Sec 4.2: Session Lifecycles)
      const isRevoked = await this.redis.get(`blacklist:${payload.jti}`);
      if (isRevoked) {
        res.status(401).json({ error: 'Token has been revoked' });
        return;
      }

      req.user = {
        id: payload.sub,
        tenantId: payload.tenantId,
        roles: payload.roles,
      };

      next();
    } catch (error) {
      this.logger.warn('Authentication failure', { error });
      res.status(401).json({ error: 'Invalid or expired credentials' });
    }
  };
}
```