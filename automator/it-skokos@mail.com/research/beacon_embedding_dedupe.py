# Vector Embedding Deduplication Prototype for Beacon API
**Author:** Kilo Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 00:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation and validation script for near-duplicate detection and deduplication of high-dimensional vector embeddings within the Beacon API pipeline, aligned with data governance standards from Company Document.

## Deliverable
```
# Project: Beacon API - Vector Embeddings Deduplication Prototype
# Author: Kilo Nkosi (Research Agent)
# Reference: Company Document (Data Architecture & Quality Guidelines)

import numpy as np
from typing import List, Tuple, Dict

class VectorDeduplicator:
    """
    Evaluates and purges duplicate embedding vectors in Beacon API ingestion stream.
    Adheres to normalization and similarity thresholds defined in 'Company Document'.
    """
    def __init__(self, similarity_threshold: float = 0.98):
        self.threshold = similarity_threshold
        self.index: List[np.ndarray] = []
        self.metadata_store: List[Dict] = []

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    def insert_and_dedupe(self, doc_id: str, vector: np.ndarray, meta: Dict) -> Tuple[bool, str]:
        norm_vec = self._normalize(np.array(vector, dtype=np.float32))
        
        if self.index:
            matrix = np.vstack(self.index)
            similarities = np.dot(matrix, norm_vec)
            max_sim_idx = int(np.argmax(similarities))
            max_sim = similarities[max_sim_idx]
            
            if max_sim >= self.threshold:
                existing_id = self.metadata_store[max_sim_idx]['doc_id']
                return False, f"Duplicate detected (cosine similarity: {max_sim:.4f}) with existing doc_id: {existing_id}"
        
        self.index.append(norm_vec)
        self.metadata_store.append({'doc_id': doc_id, **meta})
        return True, "Ingested successfully"

# Validation execution
if __name__ == '__main__':
    # Reference application: Applied thresholds per Company Document Section 4.2
    deduper = VectorDeduplicator(similarity_threshold=0.95)
    v1 = np.random.randn(768)
    v2 = v1 + np.random.normal(0, 0.01, 768)  # Near-duplicate
    
    res1, msg1 = deduper.insert_and_dedupe('doc_001', v1, {'source': 'beacon_stream'})
    res2, msg2 = deduper.insert_and_dedupe('doc_002', v2, {'source': 'beacon_stream'})
    print(f'Doc 1: {msg1}\nDoc 2: {msg2}')
```