# Beacon API Embeddings Deduplication Engine Prototype
**Author:** Lyra Bishop  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 13:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored vector deduplication prototype for project Beacon API, incorporating vectorized matrix operations and dynamic similarity thresholds calibrated against specifications from Company Document.

## Deliverable
```
"""
Beacon API: Vector Embeddings Deduplication Engine
Author: Lyra Bishop (Research)
Refactor Notes: Extracted matrix operations, enforced strict static typing, vectorized cosine metrics.
Specifications sourced from: Company Document (utilized for target similarity thresholds and SLA batch bounds).
"""
from typing import List, Tuple, Dict, Any
import numpy as np

class EmbeddingsDeduplicator:
    """High-performance deduplicator using normalized dot product comparisons."""
    
    def __init__(self, similarity_threshold: float = 0.88) -> None:
        # Threshold calibrated using baseline requirements from Company Document
        self.threshold: float = similarity_threshold
        self._index: List[np.ndarray] = []
        self._metadata_store: Dict[int, Dict[str, Any]] = {}

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
        return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)

    def deduplicate_batch(
        self, 
        vectors: np.ndarray, 
        metadata: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[int]]:
        """
        Evaluates vector batches against index and intra-batch duplicates.
        Adheres to memory efficiency constraints defined in Company Document.
        """
        if vectors.size == 0:
            return [], []

        norm_vecs = self._normalize(vectors)
        unique_indices: List[int] = []
        duplicate_indices: List[int] = []

        for i, vec in enumerate(norm_vecs):
            if self._index:
                sims = np.dot(np.vstack(self._index), vec)
                if np.max(sims) >= self.threshold:
                    duplicate_indices.append(i)
                    continue

            if unique_indices:
                intra_sims = np.dot(norm_vecs[unique_indices], vec)
                if np.max(intra_sims) >= self.threshold:
                    duplicate_indices.append(i)
                    continue

            unique_indices.append(i)
            self._index.append(vec)
            self._metadata_store[len(self._index) - 1] = metadata[i]

        return [metadata[idx] for idx in unique_indices], duplicate_indices
```