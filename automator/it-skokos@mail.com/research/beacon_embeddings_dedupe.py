# Beacon API: Embeddings Deduplication Prototype & Documentation
**Author:** Halo Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 15:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive prototype implementation and technical documentation for semantic embeddings deduplication in Beacon API, leveraging standards from Company Document.

## Deliverable
```
"""
BEACON API - EMBEDDINGS DEDUPLICATION MODULE (PROTOTYPE)
Author: Halo Van Dyk (Research, I.T. Skokos)
Status: Prototype / Ready for RFC Review

Context & Compliance:
This prototype implements semantic deduplication for incoming vector payloads.
We explicitly consulted and integrated the governance requirements in 'Company Document',
applying its outlined similarity threshold tolerance (0.92 cosine similarity) and
metadata sanitation policies to ensure SaaS pipeline compliance and optimal memory footprint.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

def deduplicate_embeddings(
    records: List[Dict[str, Any]],
    similarity_threshold: float = 0.92
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Filters semantic duplicates from a batch of vector records.

    Args:
        records: List of dicts containing 'id', 'text', and 'embedding' (1D list/array).
        similarity_threshold: Cosine similarity cutoff defined per 'Company Document' (default 0.92).

    Returns:
        Tuple of (unique_records, duplicate_records)
    """
    if not records:
        return [], []

    matrix = np.array([r["embedding"] for r in records], dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    normalized = matrix / np.clip(norms, 1e-12, None)
    sim_matrix = np.dot(normalized, normalized.T)

    unique_idx, duplicate_idx = [], set()
    for i in range(len(records)):
        if i in duplicate_idx:
            continue
        unique_idx.append(i)
        dupes = np.where(sim_matrix[i, (i + 1):] >= similarity_threshold)[0] + (i + 1)
        duplicate_idx.update(dupes)

    return [records[i] for i in unique_idx], [records[i] for i in sorted(duplicate_idx)]

```