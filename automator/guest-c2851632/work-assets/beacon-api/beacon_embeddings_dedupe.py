# Beacon API - Prototype Embeddings Deduplication Module
**Author:** Byte Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** 13/09/2026, 23:55:46  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic vector deduplication implementation for Beacon API using cosine similarity thresholds and batch clustering, aligned with specifications from Company Document.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Prototype
Author: Byte Reyes (Research)
Context: Implemented per deduplication criteria in 'Company Document' (Business Document).
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class EmbeddingDeduplicator:
    def __init__(self, similarity_threshold: float = 0.92):
        # Threshold derived from acceptance benchmarks in Company Document
        self.similarity_threshold = similarity_threshold

    def _cosine_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized = np.divide(embeddings, norms, out=np.zeros_like(embeddings), where=norms != 0)
        return np.dot(normalized, normalized.T)

    def deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Partitions records into unique items and duplicates based on vector cosine similarity.
        """
        if not records:
            return [], []

        embeddings = np.array([r["embedding"] for r in records], dtype=np.float32)
        sim_matrix = self._cosine_similarity_matrix(embeddings)
        
        unique_indices = []
        duplicate_indices = []
        seen = set()

        for i in range(len(records)):
            if i in seen:
                continue
            unique_indices.append(i)
            seen.add(i)
            
            # Identify duplicates for current record
            dupes = np.where(sim_matrix[i] >= self.similarity_threshold)[0]
            for d in dupes:
                if d != i and d not in seen:
                    duplicate_indices.append(d)
                    seen.add(d)

        unique_records = [records[idx] for idx in unique_indices]
        duplicate_records = [records[idx] for idx in duplicate_indices]
        
        return unique_records, duplicate_records

```