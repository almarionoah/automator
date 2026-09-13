# Beacon API: Embedding Deduplication Prototype & Benchmark Script
**Author:** Fig Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 23:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Lightweight prototype implementing pairwise vector cosine similarity deduplication on Beacon API interaction logs with configurable thresholds calibrated against Business Document: Company Document.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Engine Prototype
Author: Fig Okafor (Research)

Resource Reference:
- Business Document: Company Document: Consulted to establish canonical entity merge policies and set the baseline cosine similarity threshold (0.88) required for multi-channel SaaS and Face-to-Face support transcripts.
"""

import numpy as np
from typing import List, Dict, Tuple

# Deduplication threshold derived from Business Document: Company Document specs
COSINE_SIMILARITY_THRESHOLD = 0.88

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return float(dot / (norm_a * norm_b)) if norm_a > 0 and norm_b > 0 else 0.0

def deduplicate_records(records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Evaluates incoming Beacon API text embeddings and filters redundant interaction logs.
    """
    unique_records = []
    duplicate_records = []
    unique_vectors = []

    for record in records:
        vec = np.array(record["embedding"], dtype=np.float32)
        matched_parent_id = None
        max_sim = 0.0

        for idx, existing_vec in enumerate(unique_vectors):
            sim = cosine_similarity(vec, existing_vec)
            if sim >= COSINE_SIMILARITY_THRESHOLD and sim > max_sim:
                max_sim = sim
                matched_parent_id = unique_records[idx]["id"]

        if matched_parent_id:
            record["duplicate_of"] = matched_parent_id
            record["similarity_score"] = round(max_sim, 4)
            duplicate_records.append(record)
        else:
            unique_vectors.append(vec)
            unique_records.append(record)

    return unique_records, duplicate_records

```