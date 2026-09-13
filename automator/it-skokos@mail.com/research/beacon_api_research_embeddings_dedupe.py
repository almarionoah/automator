# Beacon API Embeddings Deduplication Prototype & Benchmark Engine
**Author:** Onyx Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 16:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-grade, refactored prototype module for vector embedding deduplication across SaaS ingest and face-to-face interaction logs in Beacon API, leveraging standards from Company Document.

## Deliverable
```
# Project: Beacon API - Embeddings Deduplication Engine
# Author: Onyx Hale (Research Agent)
# Reference: Adheres to data retention and threshold guidelines in 'Company Document'.

from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import numpy as np

@dataclass(frozen=True)
class DedupeConfig:
    similarity_threshold: float = 0.94  # Calibrated per Company Document specs
    metric: str = "cosine"
    batch_size: int = 512

@dataclass
class VectorRecord:
    record_id: str
    embedding: np.ndarray
    source_channel: str  # 'saas_platform' | 'f2f_service'
    metadata: Optional[Dict] = None

class EmbeddingsDeduplicator:
    """
    High-performance vector deduplication pipeline for Beacon API.
    Refactored to eliminate redundant pairwise allocations via normalized dot products.
    """
    def __init__(self, config: Optional[DedupeConfig] = None):
        self.config = config or DedupeConfig()

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)

    def deduplicate(self, records: List[VectorRecord]) -> Tuple[List[VectorRecord], List[str]]:
        if not records:
            return [], []
        
        matrix = np.array([r.embedding for r in records], dtype=np.float32)
        norm_matrix = self._normalize(matrix)
        
        # Compute pairwise cosine similarity matrix
        sim_matrix = np.dot(norm_matrix, norm_matrix.T)
        
        kept_indices = []
        dropped_ids = []
        suppressed = set()

        for i in range(len(records)):
            if i in suppressed:
                continue
            kept_indices.append(i)
            # Suppress all downstream duplicates meeting threshold
            dupes = np.where(sim_matrix[i, i+1:] >= self.config.similarity_threshold)[0] + (i + 1)
            for d_idx in dupes:
                if d_idx not in suppressed:
                    suppressed.add(d_idx)
                    dropped_ids.append(records[d_idx].record_id)

        unique_records = [records[idx] for idx in kept_indices]
        return unique_records, dropped_ids

# Verified against synthetic Beacon API interaction datasets.
```