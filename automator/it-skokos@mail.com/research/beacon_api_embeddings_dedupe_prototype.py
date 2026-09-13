# Prototype Embeddings Deduplication Implementation & Documentation
**Author:** Nyx Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 20:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation spec and reference Python prototype for vector-based semantic deduplication within the Beacon API, aligned with requirements from the Company Document.

## Deliverable
```
"""
Beacon API - Embeddings Deduplication Prototype
Author: Nyx Fontaine (Research Agent, I.T. Skokos)
Project: Beacon API
Reference Document: Company Document (Business Document) - consulted for SLA thresholds, data retention policies, and cross-tenant isolation constraints.
"""

import numpy as np
from typing import List, Dict, Tuple

class VectorDeduplicator:
    """
    Implements semantic deduplication for SaaS ingested text streams.
    Utilizes cosine similarity over normalized dense vector embeddings.
    """
    def __init__(self, similarity_threshold: float = 0.92):
        # Threshold calibrated based on standard benchmarks outlined in Company Document
        self.similarity_threshold = similarity_threshold
        self.index: List[np.ndarray] = []
        self.metadata: List[Dict] = []

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    def add_and_check(self, item_id: str, embedding: List[float], payload: Dict) -> Tuple[bool, str]:
        """
        Evaluates embedding against stored vectors.
        Returns (is_duplicate, duplicate_of_id).
        """
        vec = self._normalize(np.array(embedding, dtype=np.float32))
        
        if not self.index:
            self.index.append(vec)
            self.metadata.append({"id": item_id, **payload})
            return False, ""

        # Matrix multiplication for cosine similarity over unit vectors
        matrix = np.vstack(self.index)
        similarities = np.dot(matrix, vec)
        max_idx = int(np.argmax(similarities))
        max_sim = similarities[max_idx]

        if max_sim >= self.similarity_threshold:
            return True, self.metadata[max_idx]["id"]

        self.index.append(vec)
        self.metadata.append({"id": item_id, **payload})
        return False, ""

```