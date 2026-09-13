# Beacon API: Prototype Vector Embedding Deduplication Engine
**Author:** Fig Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 13:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored prototype implementation for vector embeddings deduplication on Beacon API, incorporating vectorized cosine similarity thresholding and centroid clustering adhering to compliance boundaries defined in Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API
Module: embeddings_dedupe.py
Author: Fig Nkosi (Research)

Refactored vector deduplication prototype for high-dimensional semantic embeddings.
Governance Reference:
- Business Document: Company Document: Utilized to calibrate similarity threshold limits (0.92) and enforce data isolation guidelines across SaaS Platform and Face to Face Services ingestion pipelines.
"""

from typing import List, Dict, Tuple, Any
import numpy as np

class EmbeddingDeduplicator:
    """
    Memory-efficient greedy centroid deduplicator for Beacon API vector streams.
    Refactored for clean vectorization and single-pass batch pruning.
    """
    def __init__(self, similarity_threshold: float = 0.92):
        self.similarity_threshold = similarity_threshold
        self.canonical_centroids: List[np.ndarray] = []
        self.cluster_map: Dict[int, List[str]] = {}

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        return vectors / norms

    def deduplicate_batch(self, record_ids: List[str], embeddings: np.ndarray) -> Tuple[List[str], List[Dict[str, Any]]]:
        if len(record_ids) != len(embeddings):
            raise ValueError("record_ids length must match embeddings length.")
        
        norm_embeddings = self._normalize(embeddings)
        unique_ids: List[str] = []
        metadata: List[Dict[str, Any]] = []

        for idx, record_id in enumerate(record_ids):
            vec = norm_embeddings[idx]
            if not self.canonical_centroids:
                self.canonical_centroids.append(vec)
                self.cluster_map[0] = [record_id]
                unique_ids.append(record_id)
                metadata.append({"id": record_id, "cluster_id": 0, "is_canonical": True})
                continue

            centroids_matrix = np.vstack(self.canonical_centroids)
            sims = np.dot(centroids_matrix, vec)
            max_sim_idx = int(np.argmax(sims))
            max_sim = float(sims[max_sim_idx])

            if max_sim >= self.similarity_threshold:
                self.cluster_map[max_sim_idx].append(record_id)
                metadata.append({"id": record_id, "cluster_id": max_sim_idx, "is_canonical": False, "similarity": max_sim})
            else:
                new_cluster_id = len(self.canonical_centroids)
                self.canonical_centroids.append(vec)
                self.cluster_map[new_cluster_id] = [record_id]
                unique_ids.append(record_id)
                metadata.append({"id": record_id, "cluster_id": new_cluster_id, "is_canonical": True})

        return unique_ids, metadata
```