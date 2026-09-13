# Beacon API Embeddings Deduplication Prototype & Security Validation Spec
**Author:** Prism Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 14:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of high-performance cosine similarity deduplication for vector embeddings within Beacon API, incorporating input validation and memory-safe boundary checks based on internal governance guidelines.

## Deliverable
```
"""
Beacon API - Embeddings Deduplication Engine Prototype
Author: Prism Reyes (Research / Security Paranoid)
Reference: Company Document (Section 4.2: Data Handling & Ephemeral Vector Sanitization)

Usage Notes:
- Uses strict threshold-based cosine similarity to reject near-duplicate embeddings.
- In accordance with 'Company Document', all inbound vectors are validated for dimension integrity (1536-d) and sanitized before memory allocation to prevent side-channel leakage.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class SecureEmbeddingDeduplicator:
    def __init__(self, similarity_threshold: float = 0.95, expected_dim: int = 1536):
        # Defense-in-depth: strict parameter bounds
        if not (0.0 < similarity_threshold < 1.0):
            raise ValueError("Security Exception: similarity_threshold out of valid bounds (0.0, 1.0).")
        self.threshold = similarity_threshold
        self.expected_dim = expected_dim
        self._index: List[np.ndarray] = []
        self._metadata_registry: List[Dict[str, Any]] = []

    def _validate_vector(self, vector: List[float]) -> np.ndarray:
        # Guard against malformed payloads / memory overflow
        if len(vector) != self.expected_dim:
            raise ValueError(f"Payload rejected: Vector dimension {len(vector)} != expected {self.expected_dim}")
        arr = np.array(vector, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm == 0 or np.isnan(norm) or np.isinf(norm):
            raise ValueError("Security Exception: Degenerate or non-finite vector supplied.")
        return arr / norm

    def process_and_dedupe(self, doc_id: str, raw_vector: List[float], meta: Dict[str, Any]) -> Tuple[bool, str]:
        vec = self._validate_vector(raw_vector)
        for idx, existing_vec in enumerate(self._index):
            similarity = float(np.dot(vec, existing_vec))
            if similarity >= self.threshold:
                return False, f"DUPLICATE_REJECTED: Matched item {self._metadata_registry[idx]['id']} (score: {similarity:.4f})"
        self._index.append(vec)
        self._metadata_registry.append({"id": doc_id, "meta": meta})
        return True, "ACCEPTED_UNIQUE"

```