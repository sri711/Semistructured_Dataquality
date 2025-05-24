import json
from core.gemini_client import gemini_flash

PROMPT_TEMPLATE = """
You are a world-class data quality expert with deep expertise in textual coherence and semantics. You have been tasked with evaluating the **semantic coherence** of the given markdown content.

**Definition**:
Semantic coherence measures how well the ideas, topics, and meanings flow logically and meaningfully within and across sentences and paragraphs. It includes:
- **Local coherence**: Logical connection and consistent topic flow between adjacent sentences.
- **Global coherence**: Overall consistency and meaningful connection of paragraphs and sections to form a unified message or narrative.

**Instructions**:
1. Analyze the markdown content for both local and global coherence.
2. For each sentence or paragraph transition, determine whether it maintains clear, logical, and meaningful flow of ideas.
3. Identify any **incoherent**, disjointed, or unrelated transitions.
4. For each check, provide:
   - "is_coherent": true if coherent, false if incoherent or inconsistent.
   - "issue": null if coherent, otherwise a brief explanation of the inconsistency.

**Expected Output**:
Return only a **JSON list**, where each element contains:
- "segment": The sentence or paragraph transition being evaluated
- "is_coherent": Boolean true/false
- "issue": Explanation if incoherent, or null

Do not enclose the JSON output in triple quotes.

Markdown content to analyze:
\"\"\"{content}\"\"\"
"""

async def evaluate_semantic_coherence(markdown: str):
    prompt = PROMPT_TEMPLATE.format(content=markdown)
    response = await gemini_flash(prompt)

    try:
        results = json.loads(response)
    except Exception as e:
        return f"❌ Failed to parse Gemini response as JSON:\n{response}\nError: {e}"

    total = len(results)
    incoherent_count = sum(1 for item in results if item.get("is_coherent") is False)
    score = round(1 - (incoherent_count / total), 2) if total > 0 else 0.0

    print("\n🔎 Semantic Coherence Agent Output:")
    print(json.dumps(results, indent=2))
    print(f"\n✅ Calculated Semantic Coherence Score: 1 - ({incoherent_count}/{total}) = {score}\n")

    return {
        "score": score,
        "total_checks": total,
        "coherent_checks": total - incoherent_count,
        "incoherent_checks": incoherent_count,
        "details": results
    }
