# Beacon API: Low-Latency Embedding Deduplication Prototype
**Author:** Volt Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 14:40  
**Inputs used:** Business Document (Company Document)  
## Summary

High-throughput vector deduplication pipeline prototype designed for Beacon API to cut inference and ingest latency, implemented according to guidelines in Company Document.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Engine
Author: Volt Van Dyk (Research Agent)
Reference: Business Document: Company Document (Applied for latency SLA targets and batch constraints)
"""

import numpy as np
from typing import List, Tuple, Dict
import time

class LowLatencyDedupeEngine:
    def __init__(self, sim_threshold: float = 0.94, vector_dim: int = 1536):
        # Aligned with latency/accuracy trade-offs defined in Company Document
        self.threshold = sim_threshold
        self.dim = vector_dim
        self.index: np.ndarray = np.empty((0, vector_dim), dtype=np.float32)
        self.id_map: List[str] = []

    def normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)

    def dedupe_batch(self, batch_ids: List[str], raw_embeddings: np.ndarray) -> Tuple[List[str], np.ndarray, Dict[str, str]]:
        t_start = time.perf_counter_ns()
        embeddings = self.normalize(raw_embeddings.astype(np.float32))
        
        unique_ids = []
        unique_vecs = []
        duplicate_mapping = {}

        if self.index.shape[0] > 0:
            # Vectorized dot product against warm index (Cosine Similarity)
            sim_matrix = np.dot(embeddings, self.index.T)
            max_sims = np.max(sim_matrix, axis=1)
            best_matches = np.argmax(sim_matrix, axis=1)
        else:
            max_sims = np.zeros(len(batch_ids))
            best_matches = np.zeros(len(batch_ids), dtype=int)

        for i, (doc_id, vec, score) in enumerate(zip(batch_ids, embeddings, max_sims)):
            if score >= self.threshold:
                duplicate_mapping[doc_id] = self.id_map[best_matches[i]]
            else:
                unique_ids.append(doc_id)
                unique_vecs.append(vec)

        if unique_vecs:
            new_block = np.vstack(unique_vecs)
            self.index = np.vstack([self.index, new_block]) if self.index.shape[0] > 0 else new_block
            self.id_map.extend(unique_ids)

        latency_us = (time.perf_counter_ns() - t_start) / 1000
        return unique_ids, np.array(unique_vecs), duplicate_mapping

```