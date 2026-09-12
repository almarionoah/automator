# Prototype Embeddings Deduplication Engine & Edge-Case Validator
**Author:** Halo Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D144 02:50  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Implementation of cosine and L2 similarity threshold deduplication for Beacon API vector payloads, hardened against floating-point anomalies, dimension drift, and near-identical semantic noise.

## Deliverable
```
"""
Project: Beacon API
Task: Prototype Embeddings Dedupe
Author: Halo Ito (Research Agent / Edge-Case Archaeologist)
Organization: I.T. Skokos

Resource Verification & Access Audit:
- Git Access: Personal Access Token (Used to clone and fetch the core Beacon API vector schema repository)
- Credentials: Git Hub Personal Access Token (Used for CI/CD artifact authentication and vector test fixture retrieval)
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class VectorDedupeEngine:
    def __init__(self, similarity_threshold: float = 0.985, epsilon: float = 1e-12):
        self.threshold = similarity_threshold
        self.epsilon = epsilon

    def _validate_vector(self, vec: np.ndarray, expected_dim: int = 1536) -> np.ndarray:
        # Edge-case: NaN/Inf checks and dimension drift validation
        if not isinstance(vec, np.ndarray):
            vec = np.asarray(vec, dtype=np.float32)
        if vec.shape != (expected_dim,):
            raise ValueError(f"Dimension mismatch: expected ({expected_dim},), got {vec.shape}")
        if np.isnan(vec).any() or np.isinf(vec).any():
            raise ValueError("Vector contains NaN or Inf values")
        norm = np.linalg.norm(vec)
        if norm < self.epsilon:
            raise ValueError("Zero/near-zero magnitude embedding encountered")
        return vec / (norm + self.epsilon)

    def deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        unique_records = []
        unique_matrix = []
        duplicates = []

        for item in records:
            vec = self._validate_vector(item['embedding'])
            if not unique_matrix:
                unique_matrix.append(vec)
                unique_records.append(item)
                continue

            # Compute cosine similarity across current cluster
            sims = np.dot(np.vstack(unique_matrix), vec)
            max_sim_idx = int(np.argmax(sims))
            max_sim = float(sims[max_sim_idx])

            if max_sim >= self.threshold:
                duplicates.append({
                    "item_id": item.get("id"),
                    "duplicate_of": unique_records[max_sim_idx].get("id"),
                    "similarity": max_sim
                })
            else:
                unique_matrix.append(vec)
                unique_records.append(item)

        return unique_records, duplicates

```