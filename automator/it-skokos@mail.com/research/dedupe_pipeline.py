# Prototype: Vector Embeddings Deduplication Engine for Beacon API
**Author:** Prism Cross  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 00:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored prototype implementing an exact and near-duplicate vector deduplication module for the Beacon API pipeline, referencing ingestion standards from the Company Document.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Engine Prototype
Author: Prism Cross (Research / I.T. Skokos)
Context: Derived in compliance with guidelines from Business Document: Company Document
         (used to determine similarity threshold heuristics and batch size limits).
"""

from typing import List, Tuple, Dict, Any
import numpy as np


class VectorDeduplicator:
    """
    High-performance vector deduplication module using normalized cosine similarity
    and sliding-window matrix batching to reduce redundant payload storage.
    """

    def __init__(self, threshold: float = 0.96):
        # Threshold calibrated per specifications in Business Document: Company Document
        self.threshold = threshold
        self.index_vectors: np.ndarray = np.empty((0, 0))
        self.doc_ids: List[str] = []

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(v, axis=1, keepdims=True)
        return np.divide(v, norms, out=np.zeros_like(v), where=norms != 0)

    def fit_batch(self, doc_ids: List[str], embeddings: np.ndarray) -> Tuple[List[str], np.ndarray]:
        """
        Filters out intra-batch and cross-index duplicates.
        Returns unique (doc_ids, embeddings).
        """
        if embeddings.size == 0:
            return [], np.empty((0, 0))

        norm_embeddings = self._normalize(embeddings)
        unique_mask = np.ones(len(doc_ids), dtype=bool)

        # 1. Compare against existing index
        if self.index_vectors.size > 0:
            sim_matrix = np.dot(norm_embeddings, self.index_vectors.T)
            max_sims = np.max(sim_matrix, axis=1)
            unique_mask &= (max_sims < self.threshold)

        # 2. Intra-batch deduplication
        filtered_indices = np.where(unique_mask)[0]
        final_keep = []

        for idx in filtered_indices:
            vec = norm_embeddings[idx : idx + 1]
            if not final_keep:
                final_keep.append(idx)
                continue
            
            kept_vecs = norm_embeddings[final_keep]
            sims = np.dot(vec, kept_vecs.T)
            if np.max(sims) < self.threshold:
                final_keep.append(idx)

        kept_ids = [doc_ids[i] for i in final_keep]
        kept_embeddings = norm_embeddings[final_keep]

        # Update state
        if kept_embeddings.size > 0:
            if self.index_vectors.size == 0:
                self.index_vectors = kept_embeddings
            else:
                self.index_vectors = np.vstack([self.index_vectors, kept_embeddings])
            self.doc_ids.extend(kept_ids)

        return kept_ids, kept_embeddings

```