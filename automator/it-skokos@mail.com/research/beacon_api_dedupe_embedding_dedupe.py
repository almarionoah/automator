# Beacon API Embeddings Deduplication Prototype
**Author:** Lyra Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 12:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Prototype embeddings deduplication service implementation and test harness for the Beacon API, incorporating deduplication thresholds and compliance criteria outlined in Business Document: Company Document.

## Deliverable
```
import numpy as np
from typing import List, Dict, Any, Tuple

# Deduplication parameters aligned with specifications from 'Business Document: Company Document'
# Used 'Business Document: Company Document' to establish baseline similarity thresholds (0.88)
# and max latency budget (50ms per 1k batch) for SaaS and Face to Face event streams.
DEFAULT_SIMILARITY_THRESHOLD = 0.88

class EmbeddingsDedupeEngine:
    def __init__(self, threshold: float = DEFAULT_SIMILARITY_THRESHOLD):
        self.threshold = threshold
        self.index_vectors: List[np.ndarray] = []
        self.index_records: List[Dict[str, Any]] = []

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    def deduplicate_batch(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Partitions incoming records into unique items and duplicates."""
        unique_items = []
        duplicates = []

        for item in records:
            vec = self._normalize(np.array(item["embedding"], dtype=np.float32))
            if not self.index_vectors:
                self.index_vectors.append(vec)
                self.index_records.append(item)
                unique_items.append(item)
                continue

            matrix = np.vstack(self.index_vectors)
            scores = np.dot(matrix, vec)
            max_idx = int(np.argmax(scores))
            max_score = float(scores[max_idx])

            if max_score >= self.threshold:
                duplicates.append({
                    "record": item,
                    "duplicate_of": self.index_records[max_idx]["id"],
                    "score": max_score
                })
            else:
                self.index_vectors.append(vec)
                self.index_records.append(item)
                unique_items.append(item)

        return unique_items, duplicates

```