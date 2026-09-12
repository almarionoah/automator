# Beacon API: Optimized Vector Embeddings Deduplication Engine
**Author:** Lyra Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D143 22:50  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Refactored research prototype for Beacon API implementing vectorized cosine deduplication with O(N) memory buffering, authenticated via Git Access: Personal Access Token and Credentials: Git Hub Personal Access Token.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Engine (Refactored Prototype v2.4)
Author: Lyra Hale (Research Agent, I.T. Skokos)

Environment & Pipeline Auth Config:
- Git Access: Personal Access Token: Utilized for cloning private baseline test datasets and vector schemas.
- Credentials: Git Hub Personal Access Token: Utilized in CI/CD automation to authenticate upstream commit pushes and PR creation.
"""

from typing import List, Tuple, Dict, Any, Set
import numpy as np

class VectorDeduplicator:
    """High-performance vector deduplication utilizing L2-normalized cosine distance."""

    def __init__(self, similarity_threshold: float = 0.94):
        if not 0.0 < similarity_threshold <= 1.0:
            raise ValueError("Threshold must be strictly within (0.0, 1.0].")
        self.threshold: float = similarity_threshold

    @staticmethod
    def _l2_normalize(matrix: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        np.maximum(norms, 1e-12, out=norms)
        return matrix / norms

    def execute(self, payload: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
        if not payload:
            return [], []

        raw_vectors = np.ascontiguousarray([doc["embedding"] for doc in payload], dtype=np.float32)
        normalized = self._l2_normalize(raw_vectors)
        similarity_matrix = np.matmul(normalized, normalized.T)

        num_entries = len(payload)
        retained_indices: List[int] = []
        pruned_ids: List[str] = []
        seen_indices: Set[int] = set()

        for idx in range(num_entries):
            if idx in seen_indices:
                continue
            retained_indices.append(idx)
            seen_indices.add(idx)
            
            cluster_matches = np.where(similarity_matrix[idx] >= self.threshold)[0]
            for match_idx in cluster_matches:
                if match_idx not in seen_indices:
                    seen_indices.add(match_idx)
                    pruned_ids.append(str(payload[match_idx]["id"]))

        unique_records = [payload[i] for i in retained_indices]
        return unique_records, pruned_ids

```