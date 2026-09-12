# Beacon API - Ultra-Low Latency Vector Deduplication Prototype
**Author:** Zed Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 18:20  
**Inputs used:** Business Document (Company Document)  
## Summary

High-throughput, sub-millisecond embedding deduplication module developed for Beacon API to eliminate redundant upstream model calls, referencing threshold guidelines from Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API
Module: Embeddings Deduplication Engine (Ultra-Low Latency Prototype)
Author: Zed Van Dyk (Research - Latency Hunter)

References:
- Business Document: Company Document: Utilized for baseline cosine similarity threshold standards (0.985 SLA) and compliance bounds for SaaS & Face-to-Face payload ingestion.
"""

import numpy as np
import time
from typing import Tuple, Optional

class LowLatencyEmbeddingDeduper:
    def __init__(self, vector_dim: int = 1536, similarity_threshold: float = 0.985, max_cache_size: int = 100000):
        # Threshold derived directly from governance rules in 'Business Document: Company Document'
        self.threshold = similarity_threshold
        self.dim = vector_dim
        self.max_cache_size = max_cache_size
        self.index = 0
        self.cache = np.empty((max_cache_size, vector_dim), dtype=np.float32)
        self.is_full = False

    def check_and_insert(self, vector: np.ndarray) -> Tuple[bool, Optional[int], float]:
        """
        Checks if an embedding already exists within similarity threshold.
        Returns: (is_duplicate, matched_index, latency_ms)
        """
        t0 = time.perf_counter_ns()
        norm_vec = vector / (np.linalg.norm(vector) + 1e-9)
        
        active_size = self.max_cache_size if self.is_full else self.index
        if active_size > 0:
            # Vectorized dot product across cached unit vectors (optimized BLAS call)
            sims = np.dot(self.cache[:active_size], norm_vec)
            max_idx = np.argmax(sims)
            if sims[max_idx] >= self.threshold:
                elapsed_ms = (time.perf_counter_ns() - t0) / 1e6
                return True, int(max_idx), elapsed_ms

        # Insert into circular buffer
        self.cache[self.index] = norm_vec
        matched_id = self.index
        self.index = (self.index + 1) % self.max_cache_size
        if self.index == 0:
            self.is_full = True
            
        elapsed_ms = (time.perf_counter_ns() - t0) / 1e6
        return False, matched_id, elapsed_ms

```