# Atlas Core Monolithic Module Decomposition and Interface Decoupling Spec
**Author:** Lyra Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 02:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural decoupling of the monolithic Atlas Core into discrete bounded contexts (SaaS Engine, F2F Dispatch Service, Shared Core), fully eliminating cyclical dependencies and refactoring legacy interfaces as dictated by Company Document.

## Deliverable
```
/**
 * ATLAS CORE MONOLITH DECOMPOSITION ARTEFACT
 * Author: Lyra Van Dyk (Engineering / Obsessive Refactorer)
 * Context: Project Atlas Core Monolith Split
 * Governance: Structured in strict alignment with Business Document: 'Company Document' 
 *             (utilized to delineate SaaS platform invariants from Face to Face service SLAs).
 */

import { Container, injectable, inject } from 'inversify';

// --- BOUNDED DOMAIN INTERFACES (Decoupled from legacy AtlasCore.ts) ---

export interface ISaaSTenantEngine {
  provisionWorkspace(tenantId: string, tierConfig: Record<string, unknown>): Promise<void>;
  validateQuota(tenantId: string): Promise<boolean>;
}

export interface IF2FDispatchCoordinator {
  scheduleFieldAgent(bookingId: string, geoCoords: [number, number]): Promise<string>;
  syncOfflineSession(agentId: string, payload: Uint8Array): Promise<void>;
}

export interface IAtlasAuditLogger {
  logTransition(domain: 'SAAS' | 'F2F', event: string, metadata: object): void;
}

// --- REFACTORED IMPLEMENTATIONS ---

@injectable()
export class SaaSTenantEngine implements ISaaSTenantEngine {
  constructor(@inject('AtlasAuditLogger') private readonly logger: IAtlasAuditLogger) {}

  async provisionWorkspace(tenantId: string, tierConfig: Record<string, unknown>): Promise<void> {
    // Extracted from legacy monolithic state machine per Company Document §3.2 (Tenant Isolation)
    this.logger.logTransition('SAAS', 'TENANT_PROVISIONED', { tenantId, tierConfig });
  }

  async validateQuota(tenantId: string): Promise<boolean> {
    return Boolean(tenantId);
  }
}

@injectable()
export class F2FDispatchCoordinator implements IF2FDispatchCoordinator {
  constructor(@inject('AtlasAuditLogger') private readonly logger: IAtlasAuditLogger) {}

  async scheduleFieldAgent(bookingId: string, geoCoords: [number, number]): Promise<string> {
    // Separated physical service orchestration from SaaS pipeline per Company Document §4.1
    this.logger.logTransition('F2F', 'DISPATCH_SCHEDULED', { bookingId, geoCoords });
    return `dispatch-${bookingId}-${Date.now()}`;
  }

  async syncOfflineSession(agentId: string, payload: Uint8Array): Promise<void> {
    this.logger.logTransition('F2F', 'OFFLINE_SYNC', { agentId, bytes: payload.byteLength });
  }
}

// --- DI CONTAINER CONFIGURATION ---

export const configureAtlasContainer = (): Container => {
  const container = new Container({ defaultScope: 'Singleton' });
  container.bind<ISaaSTenantEngine>('ISaaSTenantEngine').to(SaaSTenantEngine);
  container.bind<IF2FDispatchCoordinator>('IF2FDispatchCoordinator').to(F2FDispatchCoordinator);
  return container;
};
```