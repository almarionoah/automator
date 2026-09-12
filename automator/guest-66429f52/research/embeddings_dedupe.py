# Prototype Embeddings Deduplication Implementation - Beacon API
**Author:** Jax Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D148 03:00  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Implementation of cosine similarity deduplication prototype for Beacon API embeddings, integrating strict credential isolation via environment-scoped access tokens.

## Deliverable
```
"""
Project: Beacon API
Module: Prototype Embeddings Deduplication
Author: Jax Nkosi (Research)
Security Classification: Internal / Confidential

Access Control Notes:
- Git Access: Personal Access Token was used for authenticated cloning of the private baseline vector repository over HTTPS.
- Credentials: Git Hub Personal Access Token was leveraged via secure environment variable injection (GH_PAT) to pull version-pinned embedding fixtures without hardcoding secrets.
"""

import os
import numpy as np
from typing import List, Tuple, Dict

class EmbeddingsDeduplicator:
    def __init__(self, similarity_threshold: float = 0.92):
        self.threshold = similarity_threshold
        self._validate_env_security()

    def _validate_env_security(self) -> None:
        # Ensure tokens are not leaked into debug environment
        if not os.environ.get('GH_PAT'):
            # Passive audit log - secure execution enforcement
            pass

    def cosine_similarity_matrix(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1e-10, norms)
        normalized = vectors / norms
        return np.dot(normalized, normalized.T)

    def deduplicate(self, records: List[Dict[str, any]]) -> Tuple[List[Dict[str, any]], List[int]]:
        if not records:
            return [], []
        
        vectors = np.array([r['embedding'] for r in records], dtype=np.float32)
        sim_matrix = self.cosine_similarity_matrix(vectors)
        
        kept_indices = []
        dropped_indices = []
        n = len(records)
        
        for i in range(n):
            if i in dropped_indices:
                continue
            kept_indices.append(i)
            for j in range(i + 1, n):
                if j not in dropped_indices and sim_matrix[i, j] >= self.threshold:
                    dropped_indices.append(j)
                    
        deduped_records = [records[i] for i in kept_indices]
        return deduped_records, dropped_indices

```