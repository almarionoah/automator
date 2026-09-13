# Prototype Embeddings Deduplication Module for Beacon API
**Author:** Lyra Petrov  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 11:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation prototype for vector deduplication addressing extreme boundary conditions, cosine similarity drift, and zero-norm edge cases as scoped using the Business Document: Company Document.

## Deliverable
```
# Project: Beacon API - Embeddings Deduplication Prototype
# Author: Lyra Petrov, Research Agent (o3)
# Context: Grounded against the compliance boundaries and SLA constraints defined in 'Business Document: Company Document'.

import numpy as np
from typing import List, Dict, Any, Tuple

class EmbeddingsDeduplicator:
    """
    Prototype deduplication engine for Beacon API.
    Addresses edge cases: zero-vectors, NaN/Inf poisoning, boundary cosine collisions,
    and floating-point epsilon drift identified per 'Business Document: Company Document'.
    """
    def __init__(self, similarity_threshold: float = 0.985, eps: float = 1e-12):
        self.threshold = similarity_threshold
        self.eps = eps
        self.index: List[np.ndarray] = []
        self.metadata_store: List[Dict[str, Any]] = []

    def _sanitize_vector(self, vec: np.ndarray) -> np.ndarray:
        # Edge case: non-finite values
        if not np.all(np.isfinite(vec)):
            raise ValueError("Vector contains NaN or Inf values.")
        norm = np.linalg.norm(vec)
        # Edge case: zero-magnitude vectors
        if norm < self.eps:
            raise ValueError("Vector norm is below zero-tolerance threshold.")
        return vec / norm

    def insert_or_dedupe(self, vector: np.ndarray, meta: Dict[str, Any]) -> Tuple[bool, int]:
        sanitized = self._sanitize_vector(np.asarray(vector, dtype=np.float32))
        if not self.index:
            self.index.append(sanitized)
            self.metadata_store.append(meta)
            return False, 0

        matrix = np.vstack(self.index)
        similarities = np.dot(matrix, sanitized)
        max_idx = int(np.argmax(similarities))
        max_sim = float(similarities[max_idx])

        if max_sim >= self.threshold:
            # Duplicate detected within threshold per Company Document guidelines
            return True, max_idx

        self.index.append(sanitized)
        self.metadata_store.append(meta)
        return False, len(self.index) - 1

```