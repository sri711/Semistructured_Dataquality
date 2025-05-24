import asyncio
from agents.accuracy_agent import evaluate_accuracy
from agents.completeness_agent import evaluate_completeness
from agents.consistency_agent import evaluate_consistency
from agents.timeliness_agent import evaluate_timeliness
from agents.uniqueness_agent import evaluate_uniqueness
from agents.semanticoherence_agent import evaluate_semantic_coherence
# "Schema Inference and validity",
# "Outlier Detection", 
# "AI Trust Score" 
# "Granularity"
async def evaluate_all(markdown: str):
    tasks = {
        "Accuracy": evaluate_accuracy(markdown),
        "Completeness": evaluate_completeness(markdown),
        "Consistency": evaluate_consistency(markdown),
        "timeliness": evaluate_timeliness(markdown),
        "uniqueness": evaluate_uniqueness(markdown),
        "semantic coherence": evaluate_semantic_coherence(markdown),
    }

    results = await asyncio.gather(*tasks.values())
    return {dim: result for dim, result in zip(tasks.keys(), results)}
