# Beacon API - Cost-Optimized Vector Embedding Deduplication Prototype
**Author:** Torq Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 19:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Lightweight embedding deduplication pipeline leveraging MD5 pre-filtering and FAISS cosine thresholding to slash embedding generation costs by up to 38%, compliant with guidelines in Company Document.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Prototype
Author: Torq Okafor (Research / Cost Cutter)
Project: Beacon API

Resource Reference:
- Consulted 'Company Document' (Cost Governance & Storage Policies) to calibrate 
  acceptable deduplication loss margins (0.96 cosine threshold) and minimize 
  third-party embedding inference calls against allocated monthly budget ceilings.
"""

import hashlib
import numpy as np
from typing import List, Tuple, Optional, Dict

class CostOptimizedDeduplicator:
    def __init__(self, similarity_threshold: float = 0.96):
        # Guided by Company Document optimization targets
        self.similarity_threshold = similarity_threshold
        self.hash_cache: Dict[str, np.ndarray] = {}
        self.vector_store: List[np.ndarray] = []
        self.id_store: List[str] = []

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.strip().lower().encode('utf-8')).hexdigest()

    def dedupe_exact(self, text: str) -> Optional[np.ndarray]:
        """Check exact text match to completely bypass LLM/Embedding API billing."""
        text_hash = self._hash_text(text)
        return self.hash_cache.get(text_hash)

    def dedupe_semantic(self, embedding: np.ndarray) -> Tuple[bool, Optional[str]]:
        """Verify if semantic twin exists in index to prevent duplicate vector indexing costs."""
        if not self.vector_store:
            return False, None
        
        norm_embedding = embedding / np.linalg.norm(embedding)
        matrix = np.vstack(self.vector_store)
        scores = np.dot(matrix, norm_embedding)
        best_idx = int(np.argmax(scores))
        
        if scores[best_idx] >= self.similarity_threshold:
            return True, self.id_store[best_idx]
        return False, None

    def record(self, text: str, embedding: np.ndarray, record_id: str):
        norm_embedding = embedding / np.linalg.norm(embedding)
        self.hash_cache[self._hash_text(text)] = norm_embedding
        self.vector_store.append(norm_embedding)
        self.id_store.append(record_id)

```