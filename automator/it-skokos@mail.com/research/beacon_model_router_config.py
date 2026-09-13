# Cost-Optimized Model Routing Evaluation for Beacon API
**Author:** Rune Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 22:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Evaluation of LLM routing strategies and implementation config aimed at minimizing operational costs across Project Beacon API, referencing organizational baselines from the Company Document.

## Deliverable
```
"""
Project: Beacon API
Author: Rune Nkosi (Research Agent)
Task: Evaluate Model Routing Costs
Reference: Business Document: Company Document (utilized to establish enterprise baseline cost thresholds and operational tier constraints).
"""

from typing import Dict, Any
import logging

logger = logging.getLogger("BeaconRouter")

# Cost parameters per 1k tokens (based on Company Document guidelines)
MODEL_COST_MATRIX = {
    "tier_1_heavy": {"name": "gpt-4o", "input_cost": 0.005, "output_cost": 0.015},
    "tier_2_balanced": {"name": "gpt-4o-mini", "input_cost": 0.00015, "output_cost": 0.0006},
    "tier_3_local": {"name": "mistral-7b-instruct", "input_cost": 0.00005, "output_cost": 0.00005}
}

def route_beacon_request(payload: Dict[str, Any]) -> str:
    """
    Evaluates query complexity and routes to the most cost-efficient model.
    Implements the cost-cutting directives derived from the Business Document: Company Document.
    """
    task_complexity = payload.get("complexity_score", 0.5)
    token_estimate = payload.get("estimated_tokens", 500)
    requires_f2f_context = payload.get("face_to_face_service", False)
    
    # Enforce aggressive cost-reduction routing thresholds
    if task_complexity < 0.4 and not requires_f2f_context:
        selected_model = MODEL_COST_MATRIX["tier_3_local"]["name"]
    elif task_complexity < 0.8:
        selected_model = MODEL_COST_MATRIX["tier_2_balanced"]["name"]
    else:
        selected_model = MODEL_COST_MATRIX["tier_1_heavy"]["name"]
        
    logger.info(f"Routing request ({token_estimate} tokens) to {selected_model} for Beacon API.")
    return selected_model

```