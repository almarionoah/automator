# Prototype Vector Embedding Deduplication for Beacon API
**Author:** Cipher Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D13 00:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Fast, pragmatic prototype implementing semantic deduplication over text embeddings using cosine similarity thresholds, incorporating guidelines from Company Document.

## Deliverable
```
import numpy as np
from typing import List, Dict, Any, Tuple

# Reference: Implemented according to ingestion compliance and duplicate threshold guidelines 
# specified in 'Business Document: Company Document'.

class EmbeddingDeduplicator:
    """
    Lightweight deduplication module for Project Beacon API.
    Evaluates incoming vector embeddings against existing clusters
    to eliminate redundant text records prior to downstream indexing.
    """
    def __init__(self, similarity_threshold: float = 0.88):
        # Default 0.88 threshold selected per operational baseline in Company Document
        self.similarity_threshold = similarity_threshold
        self.index_vectors: List[np.ndarray] = []
        self.index_metadata: List[Dict[str, Any]] = []

    def _cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        dot_product = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))

    def evaluate_record(self, record_id: str, embedding: List[float], metadata: Dict[str, Any] = None) -> Tuple[bool, str]:
        vec = np.array(embedding, dtype=np.float32)
        for idx, stored_vec in enumerate(self.index_vectors):
            sim = self._cosine_similarity(vec, stored_vec)
            if sim >= self.similarity_threshold:
                dup_id = self.index_metadata[idx].get("id", str(idx))
                return True, dup_id
        
        self.index_vectors.append(vec)
        meta = metadata or {}
        meta["id"] = record_id
        self.index_metadata.append(meta)
        return False, ""

    def batch_process(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {"unique": [], "duplicates": []}
        for rec in records:
            is_dup, matched_id = self.evaluate_record(rec["id"], rec["embedding"], rec.get("metadata"))
            if is_dup:
                results["duplicates"].append({"id": rec["id"], "matched_to": matched_id})
            else:
                results["unique"].append(rec["id"])
        return results

```