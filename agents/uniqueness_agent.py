import json
from core.gemini_client import gemini_flash

PROMPT_TEMPLATE = """
You are a world-class data quality expert with deep expertise in content evaluation and prompt design. You have been tasked with evaluating the **uniqueness** of the given markdown content.

**Definition**:
Uniqueness refers to the extent to which the information provided is **non-redundant, non-repetitive**, and **distinct** in its factual contributions. Content is considered **unique** if it:
- Does not repeat the same fact, idea, or statement in different words (semantic redundancy).
- Avoids duplicating exact or near-identical facts across sections.
- Ensures each sentence contributes new, meaningful information to the document.

**Instructions**:
1. Carefully review the markdown content to detect **duplicate or semantically similar** facts or sentences.
2. For each sentence:
   - Compare it to the rest of the content.
   - Determine whether it introduces new information or simply repeats something already stated.
3. Return a list where each sentence is evaluated as:
   - `"is_unique"`: true if the sentence conveys distinct information, false if it repeats or duplicates prior content.
   - `"issue"`: null if the content is unique, otherwise a brief explanation of the duplication or similarity.

**Expected Output**:
Return only a **JSON list**, where each element contains:
- "sentence": The sentence being evaluated
- "is_unique": Boolean true/false
- "issue": Explanation if not unique, or null

Do not use triple quotes to wrap the JSON output.

Markdown content to analyze:
\"\"\"{content}\"\"\"
"""

async def evaluate_uniqueness(markdown: str):
    prompt = PROMPT_TEMPLATE.format(content=markdown)
    response = await gemini_flash(prompt)

    try:
        results = json.loads(response)
    except Exception as e:
        return f"❌ Failed to parse Gemini response as JSON:\n{response}\nError: {e}"

    total = len(results)
    redundant = sum(1 for item in results if item.get("is_unique") is False)
    score = round(1 - (redundant / total), 2) if total > 0 else 0.0

    print("\n🔎 Uniqueness Agent Output:")
    print(json.dumps(results, indent=2))
    print(f"\n✅ Calculated Uniqueness Score: 1 - ({redundant}/{total}) = {score}\n")

    return {
        "score": score,
        "total_sentences": total,
        "unique_sentences": total - redundant,
        "redundant_sentences": redundant,
        "details": results
    }
