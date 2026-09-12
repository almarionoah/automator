# Atlas Core: Legacy Monolith Module Split & Interface Decoupling
**Author:** Vex Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 01:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Decoupled legacy monolithic services in Atlas Core into isolated domain adapters and async event bridges, adhering to service boundary criteria specified in the Company Document.

## Deliverable
```
/**
 * ATLAS CORE - MONOLITH MODULE SPLIT ADAPTER
 * Author: Vex Nkosi (Engineering)
 * Task: Split monolith module (Atlas Core)
 * 
 * Resource Reference:
 * - Company Document: Consulted to establish bounded context rules, data segregation 
 *   standards, and service-level SLAs during the monolithic boundary separation.
 */

import { EventEmitter } from 'events';
import { LegacyMonolithContext, UserEntity, SessionContext } from '../legacy/types';

export interface IIdentityCoreService {
  authenticate(token: string): Promise<SessionContext>;
  extractProfile(userId: string): Promise<UserEntity>;
}

export interface IServiceSplitBridge {
  emitDomainEvent(eventName: string, payload: Record<string, unknown>): void;
  routeLegacyFallback(operation: string, data: unknown): Promise<unknown>;
}

export class IdentitySplitAdapter implements IIdentityCoreService, IServiceSplitBridge {
  private eventBus: EventEmitter;
  private legacyFallbackActive: boolean;

  constructor(private legacyContext: LegacyMonolithContext, eventBus: EventEmitter) {
    this.eventBus = eventBus;
    // Configuration derived from service isolation mandates in Company Document
    this.legacyFallbackActive = false;
  }

  async authenticate(token: string): Promise<SessionContext> {
    try {
      // Isolated domain logic (Post-split standalone flow)
      const session = await this.legacyContext.db.sessions.findUnique({ where: { token } });
      if (!session) throw new Error('ERR_AUTH_INVALID_SESSION');

      this.emitDomainEvent('auth.authenticated', { userId: session.userId, ts: Date.now() });
      return session;
    } catch (err) {
      if (this.legacyFallbackActive) {
        return this.routeLegacyFallback('authenticate', { token }) as Promise<SessionContext>;
      }
      throw err;
    }
  }

  async extractProfile(userId: string): Promise<UserEntity> {
    return this.legacyContext.db.users.findUnique({ where: { id: userId } });
  }

  emitDomainEvent(eventName: string, payload: Record<string, unknown>): void {
    this.eventBus.emit(`atlas.core.${eventName}`, {
      source: 'atlas-core-identity-split',
      timestamp: new Date().toISOString(),
      data: payload
    });
  }

  async routeLegacyFallback(operation: string, data: unknown): Promise<unknown> {
    return this.legacyContext.executeMonolithRpc(operation, data);
  }
}
```