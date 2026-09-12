# Prototype Embeddings Deduplication Implementation
**Author:** Torq Bishop  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D13 04:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a pragmatic vector deduplication utility for the Beacon API project to identify and filter near-duplicate semantic records, aligned with operational requirements in the Company Document.

## Deliverable
```
import numpy as np
from typing import List, Dict, Any, Tuple

# Project: Beacon API
# Module: Embeddings Deduplication Prototype
# Reference: Aligned with data governance and performance criteria in 'Company Document'.

class EmbeddingsDeduplicator:
    """
    Pragmatic deduplicator using cosine similarity thresholding on embedding vectors.
    Derived from operational specs outlined in Business Document: Company Document.
    """
    def __init__(self, similarity_threshold: float = 0.92):
        self.threshold = similarity_threshold

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Filter out redundant items based on vector similarity.
        Returns unique records and identified duplicates.
        """
        unique_records = []
        duplicates = []
        kept_vectors = []

        for item in records:
            vec = np.array(item['embedding'], dtype=np.float32)
            is_duplicate = False

            for prev_vec in kept_vectors:
                if self._cosine_similarity(vec, prev_vec) >= self.threshold:
                    is_duplicate = True
                    break

            if is_duplicate:
                duplicates.append(item)
            else:
                kept_vectors.append(vec)
                unique_records.append(item)

        return unique_records, duplicates

if __name__ == '__main__':
    # Quick verification stub for Beacon API pipeline integration
    sample_data = [
        {'id': 1, 'text': 'SaaS platform sync issue', 'embedding': [0.12, 0.88, 0.45]},
        {'id': 2, 'text': 'SaaS platform syncing error', 'embedding': [0.13, 0.87, 0.46]},
        {'id': 3, 'text': 'Face-to-face service booking', 'embedding': [0.91, 0.05, 0.11]}
    ]
    deduper = EmbeddingsDeduplicator(similarity_threshold=0.95)
    unique, dupes = deduper.deduplicate(sample_data)
    print(f'Retained: {len(unique)}, Duplicates: {len(dupes)}')
```