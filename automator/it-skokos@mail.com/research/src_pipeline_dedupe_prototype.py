# Prototype Embeddings Deduplication for Beacon API
**Author:** Iris Bishop  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 06:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a lightweight, vector-based semantic deduplication utility for the Beacon API intake pipeline. This prototype applies cosine distance clustering against incoming request embeddings to drop near-duplicate records before downstream processing, referencing requirements detailed in the Company Document.

## Deliverable
```
# Project: Beacon API - Embeddings Deduplication Prototype
# Author: Iris Bishop <iris.bishop@it-skokos.com>
# Context: Implements semantic deduplication based on criteria outlined in 'Company Document'.

import numpy as np
from typing import List, Dict, Any, Tuple

class VectorDeduplicator:
    """
    Evaluates incoming payload embeddings against recent working windows
    to filter redundant SaaS API submissions and offline event logs.
    Thresholding parameters derived from the 'Company Document' specifications.
    """
    def __init__(self, similarity_threshold: float = 0.92):
        self.similarity_threshold = similarity_threshold
        self.seen_vectors: List[np.ndarray] = []
        self.seen_metadata: List[Dict[str, Any]] = []

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    def process_batch(self, items: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        unique_items = []
        dropped_items = []

        for item in items:
            vec = self._normalize(np.array(item['embedding'], dtype=np.float32))
            if not self.seen_vectors:
                self.seen_vectors.append(vec)
                self.seen_metadata.append(item)
                unique_items.append(item)
                continue

            matrix = np.array(self.seen_vectors)
            similarities = np.dot(matrix, vec)
            max_sim_idx = int(np.argmax(similarities))
            max_sim = similarities[max_sim_idx]

            if max_sim >= self.similarity_threshold:
                dropped_items.append({
                    'item_id': item.get('id'),
                    'matched_with': self.seen_metadata[max_sim_idx].get('id'),
                    'similarity': float(max_sim)
                })
            else:
                self.seen_vectors.append(vec)
                self.seen_metadata.append(item)
                unique_items.append(item)

        return unique_items, dropped_items

```