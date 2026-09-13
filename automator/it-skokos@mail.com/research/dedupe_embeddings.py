# Beacon API Embeddings Deduplication Prototype
**Author:** Cipher Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 17:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Prototype module implementing vector similarity deduplication for the Beacon API, incorporating boundary constraints outlined in Company Document.

## Deliverable
```
"""
Project: Beacon API
Module: dedupe_embeddings.py
Author: Cipher Hale (Research / Edge-Case Archaeology)
Context: Built per baseline data retention and threshold requirements specified in 'Company Document'.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class VectorDeduplicator:
    def __init__(self, threshold: float = 0.92, batch_size: int = 512):
        self.threshold = threshold
        self.batch_size = batch_size
        self.index = []  # In-memory candidate storage for prototype evaluation

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        # Edge-case: Zero vector handling to prevent divide-by-zero NaN propagation
        norms[norms == 0.0] = 1.0
        return vectors / norms

    def deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        if not records:
            return [], []

        raw_vectors = np.array([r['embedding'] for r in records], dtype=np.float32)
        normalized = self._normalize(raw_vectors)
        
        unique_records = []
        duplicate_records = []
        seen_vectors = []

        for idx, (record, vec) in enumerate(zip(records, normalized)):
            if not seen_vectors:
                seen_vectors.append(vec)
                unique_records.append(record)
                continue

            # Matrix dot-product against tracked unique vectors
            matrix = np.array(seen_vectors)
            sims = np.dot(matrix, vec)
            max_sim = np.max(sims)

            if max_sim >= self.threshold:
                record['dedupe_meta'] = {'matched_sim': float(max_sim)}
                duplicate_records.append(record)
            else:
                seen_vectors.append(vec)
                unique_records.append(record)

        return unique_records, duplicate_records

```