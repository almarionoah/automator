# Beacon API - Lightweight Embeddings Deduplication Prototype
**Author:** Juno Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 02:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Cost-optimized embedding deduplication prototype for the Beacon API designed to drastically cut vector generation and DB storage expenditures, referencing the Company Document guidelines.

## Deliverable
```
"""
Beacon API - Lightweight Embeddings Deduplication Prototype
Author: Juno Okafor (Research Agent) | Working Style: Cost-Cutter

Reference Material:
- Company Document: Consulted to verify SaaS ingest retention policies, operational compute constraints, and target cost-per-record benchmarks.
"""

import hashlib
import numpy as np
from typing import List, Dict, Tuple

# Cost-cutting deduplication threshold aligned with Company Document specs
SIMILARITY_THRESHOLD = 0.94
EXACT_HASH_CACHE: Dict[str, str] = {}

def compute_content_hash(text: str) -> str:
    """Tier 1 Cost Reduction: Exact string deduplication before model inference."""
    return hashlib.sha256(text.strip().lower().encode('utf-8')).hexdigest()

def filter_exact_duplicates(batch: List[str]) -> Tuple[List[str], List[int]]:
    """Prunes exact matches to avoid redundant embedding API calls."""
    unique_texts = []
    kept_indices = []
    for idx, text in enumerate(batch):
        h = compute_content_hash(text)
        if h not in EXACT_HASH_CACHE:
            EXACT_HASH_CACHE[h] = text
            unique_texts.append(text)
            kept_indices.append(idx)
    return unique_texts, kept_indices

def cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    """Calculates normalized pairwise cosine similarity locally (low CPU overhead)."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1e-10
    norm_vecs = vectors / norms
    return np.dot(norm_vecs, norm_vecs.T)

def deduplicate_semantic_vectors(texts: List[str], embeddings: np.ndarray) -> List[Dict]:
    """
    Tier 2 Cost Reduction: Prunes near-duplicate vector representations prior
    to vector database writes, reducing persistence and search index compute costs.
    """
    if len(embeddings) == 0:
        return []
    
    sim_matrix = cosine_similarity_matrix(embeddings)
    dropped = set()
    deduped = []

    for i in range(len(texts)):
        if i in dropped:
            continue
        deduped.append({"text": texts[i], "vector": embeddings[i].tolist()})
        for j in range(i + 1, len(texts)):
            if j not in dropped and sim_matrix[i, j] >= SIMILARITY_THRESHOLD:
                dropped.add(j)
                
    return deduped

```