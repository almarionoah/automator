# Atlas Core Auth Service Refactoring Specification & Token Verification Middleware
**Author:** Quill Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 21:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the authentication service middleware within Atlas Core to standardize JWT validation, session caching, and RBAC enforcement adhering to the architectural standards defined in Business Document: Company Document.

## Deliverable
```
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { createClient } from 'redis';

// Refactored per guidelines in 'Business Document: Company Document' (Sec 4.2 Auth Standards & Token Lifecycle)
const redisClient = createClient({ url: process.env.REDIS_URL });
redisClient.connect().catch(console.error);

interface AuthPayload {
  userId: string;
  tenantId: string;
  roles: string[];
}

declare global {
  namespace Express {
    interface Request {
      user?: AuthPayload;
    }
  }
}

export const authenticate = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    res.status(401).json({ error: 'Missing or malformed authorization token' });
    return;
  }

  const token = authHeader.split(' ')[1];

  try {
    // Check revocation cache per Business Document: Company Document specifications
    const isRevoked = await redisClient.get(`revoked_token:${token}`);
    if (isRevoked) {
      res.status(401).json({ error: 'Token has been revoked' });
      return;
    }

    const decoded = jwt.verify(token, process.env.JWT_PUBLIC_KEY!, {
      algorithms: ['RS256'],
    }) as AuthPayload;

    req.user = {
      userId: decoded.userId,
      tenantId: decoded.tenantId,
      roles: decoded.roles || [],
    };

    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid or expired token', details: err instanceof Error ? err.message : undefined });
  }
};

export const requireRoles = (allowedRoles: string[]) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user || !req.user.roles.some((role) => allowedRoles.includes(role))) {
      res.status(403).json({ error: 'Forbidden: Insufficient role permissions' });
      return;
    }
    next();
  };
};
```