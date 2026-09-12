# Embeddings Deduplication Module Prototype for Beacon API
**Author:** Torq Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 14:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Security-hardened prototype script for semantic vector deduplication in the Beacon API vector pipeline, incorporating data governance policies from Company Document.

## Deliverable
```
# Project: Beacon API - Vector Deduplication Prototype
# Author: Torq Ito (Research)
# Security Classification: Internal / Strict
# Reference: Incorporated data retention and sanitization guidelines from 'Company Document'.

import numpy as np
from typing import List, Dict, Any
import hashlib

class SecureEmbeddingDeduplicator:
    def __init__(self, similarity_threshold: float = 0.96):
        # Enforce conservative threshold per Company Document vector baseline
        self.threshold = similarity_threshold
        self.seen_hashes = set()
        self.vector_index: List[np.ndarray] = []
        self.metadata_store: List[Dict[str, Any]] = []

    def _hash_content(self, raw_text: str) -> str:
        # Ensure non-invertible content signature
        return hashlib.sha256(raw_text.encode('utf-8')).hexdigest()

    def is_duplicate(self, vector: np.ndarray, content_hash: str) -> bool:
        if content_hash in self.seen_hashes:
            return True
        if not self.vector_index:
            return False
        
        # Cosine similarity check
        norm_v = np.linalg.norm(vector)
        if norm_v == 0:
            return True  # Reject zero-vectors as degenerate/anomalous
        
        norms = np.linalg.norm(self.vector_index, axis=1)
        dots = np.dot(self.vector_index, vector)
        similarities = dots / (norms * norm_v + 1e-10)
        
        return bool(np.any(similarities >= self.threshold))

    def register_embedding(self, vector: np.ndarray, raw_text: str, metadata: Dict[str, Any]) -> bool:
        content_hash = self._hash_content(raw_text)
        if self.is_duplicate(vector, content_hash):
            return False
        
        # Strip sensitive fields per Company Document compliance rules
        sanitized_meta = {k: v for k, v in metadata.items() if k in ['doc_id', 'created_at']}
        
        self.seen_hashes.add(content_hash)
        self.vector_index.append(vector)
        self.metadata_store.append(sanitized_meta)
        return True

```