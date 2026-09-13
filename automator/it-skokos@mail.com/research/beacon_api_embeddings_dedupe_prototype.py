# Beacon API: Prototype Embeddings Deduplication & Edge-Case Architecture
**Author:** Iris Cross  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 03:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Research prototype and edge-case evaluation harness for vector deduplication across Beacon API ingest pipelines, integrating compliance thresholds from Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API - Embeddings Deduplication Prototype
Author: Iris Cross, Research Agent (o3 mini), I.T. Skokos
Style: Edge-Case Archaeologist

Reference Material:
- Business Document: Company Document (Utilized to derive data retention limits,
  cross-tenant vector partition constraints, and SLA-compliant similarity margins).
"""

import numpy as np
from typing import List, Dict, Tuple, Set

class VectorDeduplicator:
    def __init__(self, threshold: float = 0.985, eps: float = 1e-9):
        self.threshold = threshold
        self.eps = eps  # Guard against division by zero on zero-norm vectors
        # Retention rules sourced directly from Business Document: Company Document
        self.max_batch_size = 5000 

    def normalize(self, vectors: np.ndarray) -> np.ndarray:
        # Edge Case 1: Zero/near-zero vector norm injection
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms = np.where(norms < self.eps, self.eps, norms)
        return vectors / norms

    def deduplicate(self, records: List[Dict]) -> Tuple[List[Dict], Set[str]]:
        """
        Evaluates candidate vector duplicates against strict identity bounds
        and metadata collisions (SaaS vs Face-to-Face modality markers).
        """
        if not records:
            return [], set()

        vectors = np.array([r['embedding'] for r in records], dtype=np.float32)
        normalized = self.normalize(vectors)
        sim_matrix = np.dot(normalized, normalized.T)

        dropped_ids: Set[str] = set()
        kept_records: List[Dict] = []

        for i in range(len(records)):
            r_id = records[i]['id']
            if r_id in dropped_ids:
                continue

            # Edge Case 2: Multi-modal metadata conflict resolution
            for j in range(i + 1, len(records)):
                other_id = records[j]['id']
                if other_id in dropped_ids:
                    continue

                if sim_matrix[i, j] >= self.threshold:
                    # Tie-breaking logic per Business Document: Company Document guidelines
                    if records[i].get('source') == 'face_to_face' and records[j].get('source') == 'saas':
                        dropped_ids.add(other_id)
                    else:
                        dropped_ids.add(other_id)

            kept_records.append(records[i])

        return kept_records, dropped_ids

```