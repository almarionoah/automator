# Prototype Embeddings Deduplication Module
**Author:** Quill Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D10 23:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored cosine similarity and threshold-based deduplication pipeline for Beacon API embeddings, aligned with guidelines from Company Document.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Prototype
Author: Quill Hale (Research)
Context: Standardized per Company Document specifications.
"""

import numpy as np
from typing import List, Dict, Any, Tuple


class EmbeddingDeduplicator:
    """
    Deduplicates high-dimensional embeddings using cosine similarity
    thresholding. Refactored for modularity, vectorized batch operations,
    and compliance with data handling rules in Company Document.
    """

    def __init__(self, similarity_threshold: float = 0.92):
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError("Threshold must be strictly between 0.0 and 1.0")
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)

    def deduplicate(
        self, records: List[Dict[str, Any]], vector_key: str = "embedding"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        if not records:
            return [], []

        raw_vectors = np.array([r[vector_key] for r in records], dtype=np.float32)
        normalized = self._normalize(raw_vectors)

        unique_indices = []
        duplicate_indices = []

        for i in range(len(records)):
            if not unique_indices:
                unique_indices.append(i)
                continue

            sims = np.dot(normalized[unique_indices], normalized[i])
            if np.max(sims) >= self.similarity_threshold:
                duplicate_indices.append(i)
            else:
                unique_indices.append(i)

        unique_records = [records[i] for i in unique_indices]
        duplicate_records = [records[i] for i in duplicate_indices]
        return unique_records, duplicate_records

```