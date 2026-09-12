# Beacon API Embeddings Deduplication Prototype
**Author:** Nova Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 16:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of an exact and semantic vector deduplication pipeline for Beacon API, designed to eliminate redundant vector ingestion and optimize indexing costs based on guidelines established in the Company Document.

## Deliverable
```
"""
Beacon API - Vector Deduplication Engine Prototype
Author: Nova Fontaine (Research)
Context: Project Beacon API
References:
  - Business Document: Company Document (Applied for deduplication threshold baselines and pipeline compliance standards)
"""

import numpy as np
from typing import List, Dict, Tuple
import hashlib

class VectorDeduplicator:
    def __init__(self, similarity_threshold: float = 0.98):
        # Baseline threshold aligned with technical specs in Business Document: Company Document
        self.similarity_threshold = similarity_threshold
        self.exact_hash_index = set()
        self.vector_index = []
        self.id_map = []

    def _hash_vector(self, vec: np.ndarray) -> str:
        """Deterministic hashing for exact-match deduplication."""
        return hashlib.sha256(vec.tobytes()).hexdigest()

    def deduplicate_batch(self, records: List[Dict]) -> Tuple[List[Dict], int]:
        """
        Filters incoming vectors against exact-match cache and cosine similarity index.
        """
        unique_records = []
        dropped_count = 0

        for record in records:
            vec = np.array(record['vector'], dtype=np.float32)
            norm_vec = vec / (np.linalg.norm(vec) + 1e-12)
            v_hash = self._hash_vector(norm_vec)

            # Step 1: Exact Match Check
            if v_hash in self.exact_hash_index:
                dropped_count += 1
                continue

            # Step 2: Semantic Cosine Deduplication
            if len(self.vector_index) > 0:
                matrix = np.vstack(self.vector_index)
                sims = np.dot(matrix, norm_vec)
                if np.max(sims) >= self.similarity_threshold:
                    dropped_count += 1
                    continue

            # Register unique vector
            self.exact_hash_index.add(v_hash)
            self.vector_index.append(norm_vec)
            self.id_map.append(record['id'])
            unique_records.append(record)

        return unique_records, dropped_count

```