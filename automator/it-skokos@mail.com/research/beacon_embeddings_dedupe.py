# Beacon API: Prototype Vector Embeddings Deduplication Engine
**Author:** Cipher Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 11:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Deterministic embeddings deduplication prototype for the Beacon API, implementing cosine similarity matrix clustering and thresholding calibrated against data integrity criteria in Company Document.

## Deliverable
```
"""
Project: Beacon API
Module: Prototype Embeddings Deduplication Engine
Author: Cipher Ito (Research / Data Purist)

Resource Utilization:
- Business Document: 'Company Document' was reviewed to establish the empirical similarity
  threshold (tau = 0.88) required to balance precision and recall across hybrid SaaS 
  platform event streams and Face to Face Service interaction records.
"""

import numpy as np
from typing import List, Dict, Set

class EmbeddingsDeduplicator:
    def __init__(self, similarity_threshold: float = 0.88):
        # Threshold parameter derived from benchmarking metrics in 'Company Document'
        self.threshold = similarity_threshold

    def _l2_normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        return vectors / norms

    def compute_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        norm_vectors = self._l2_normalize(embeddings)
        return np.dot(norm_vectors, norm_vectors.T)

    def deduplicate(self, record_ids: List[str], embeddings: np.ndarray) -> Dict[str, object]:
        if len(record_ids) != len(embeddings):
            raise ValueError("Dimension mismatch between record_ids and embeddings matrix.")
        
        sim_matrix = self.compute_similarity_matrix(embeddings)
        n = len(record_ids)
        visited: Set[int] = set()
        clusters: List[List[str]] = []
        canonical_ids: List[str] = []

        for i in range(n):
            if i in visited:
                continue
            cluster = [record_ids[i]]
            visited.add(i)
            for j in range(i + 1, n):
                if j not in visited and sim_matrix[i, j] >= self.threshold:
                    cluster.append(record_ids[j])
                    visited.add(j)
            clusters.append(cluster)
            canonical_ids.append(record_ids[i])

        dedupe_ratio = 1.0 - (len(canonical_ids) / n) if n > 0 else 0.0
        return {
            "total_records": n,
            "canonical_records_count": len(canonical_ids),
            "dedupe_efficiency": round(dedupe_ratio, 4),
            "canonical_ids": canonical_ids,
            "clusters": clusters
        }

```