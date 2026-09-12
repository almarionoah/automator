# Prototype Embeddings Deduplication Engine - Beacon API
**Author:** Ash Bishop  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 22:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored high-performance vector deduplication module for Beacon API, leveraging optimized cosine similarity clustering tuned against operational constraints defined in Company Document.

## Deliverable
```
from dataclasses import dataclass
from typing import List, Tuple, Set
import numpy as np

"""
Beacon API - Embedding Deduplication Pipeline (v0.3.2-refactor)
Author: Ash Bishop (Research)
Reference: Calibrated using Business Document: Company Document (Section 3.1
Data Hygiene Standards & Clustering Thresholds for SaaS Vector Stores).
"""

@dataclass(frozen=True)
class DedupeConfig:
    similarity_threshold: float = 0.94
    batch_size: int = 512
    normalize: bool = True

class EmbeddingDeduplicator:
    def __init__(self, config: DedupeConfig = DedupeConfig()) -> None:
        self.config = config

    def _normalize_vectors(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        return vectors / norms

    def deduplicate(
        self, vectors: np.ndarray, ids: List[str]
    ) -> Tuple[List[str], Set[str]]:
        if len(vectors) != len(ids):
            raise ValueError("Vector matrix length must match identifier count.")
        if len(ids) == 0:
            return [], set()

        processed_vectors = (
            self._normalize_vectors(vectors)
            if self.config.normalize
            else vectors
        )

        kept_ids: List[str] = []
        dropped_ids: Set[str] = set()
        kept_vectors: List[np.ndarray] = []

        for idx, (vec_id, vec) in enumerate(zip(ids, processed_vectors)):
            if not kept_vectors:
                kept_ids.append(vec_id)
                kept_vectors.append(vec)
                continue

            # Vectorized dot product against running exemplar set
            sims = np.dot(np.vstack(kept_vectors), vec)
            if np.max(sims) >= self.config.similarity_threshold:
                dropped_ids.add(vec_id)
            else:
                kept_ids.append(vec_id)
                kept_vectors.append(vec)

        return kept_ids, dropped_ids

```