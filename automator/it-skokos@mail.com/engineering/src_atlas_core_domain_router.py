# Atlas Core Monolith Module Decomposition
**Author:** Torq Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 16:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Successfully decomposed the Atlas Core monolith module into decoupled SaaS Platform and Face-to-Face service submodules, establishing distinct interface boundaries based on domain guidelines in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Modular Service Registry & Interface Router
Author: Torq Nkosi
Context: Decomposes monolithic Atlas Core into distinct domain packages.
Reference: Architectural constraints and boundary specifications derived directly from 'Business Document: Company Document'.
"""

from typing import Dict, Any, Protocol
import logging

logger = logging.getLogger("atlas_core.router")


class SaaSPlatformService(Protocol):
    def execute_saas_workflow(self, tenant_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...


class FaceToFaceService(Protocol):
    def coordinate_f2f_session(self, session_id: str, location_meta: Dict[str, Any]) -> Dict[str, Any]:
        ...


class AtlasCoreDomainRegistry:
    """
    Decoupled service registry replacing legacy monolithic controller.
    Boundaries aligned with Business Document: Company Document.
    """

    def __init__(self) -> None:
        self._saas_handler: SaaSPlatformService | None = None
        self._f2f_handler: FaceToFaceService | None = None

    def register_saas_handler(self, handler: SaaSPlatformService) -> None:
        self._saas_handler = handler
        logger.info("SaaS Platform module registered successfully.")

    def register_f2f_handler(self, handler: FaceToFaceService) -> None:
        self._f2f_handler = handler
        logger.info("Face-to-Face Services module registered successfully.")

    def route_request(self, domain: str, event_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if domain == "saas":
            if not self._saas_handler:
                raise RuntimeError("SaaS handler uninitialized.")
            return self._saas_handler.execute_saas_workflow(event_id, data)
        elif domain == "f2f":
            if not self._f2f_handler:
                raise RuntimeError("F2F handler uninitialized.")
            return self._f2f_handler.coordinate_f2f_session(event_id, data)
        else:
            raise ValueError(f"Unknown domain partition: {domain}")

```