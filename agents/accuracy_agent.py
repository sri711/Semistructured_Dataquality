import json
from core.gemini_client import gemini_flash
from core.markdown_utils import chunk_markdown

PROMPT_TEMPLATE = """
You are a world-class data quality expert with deep expertise in factual accuracy assessment and prompt design. You have been tasked with evaluating the **accuracy** of the given markdown content.

**Definition**:
Accuracy refers to how closely a statement (fact) aligns with objective truth, real-world facts, or commonly accepted knowledge. A fact is considered **accurate** if it is true, plausible, and free from errors, exaggeration, or misleading implications.

**Instructions**:
1. The content below has been chunked into individual sentences. Each sentence should be treated as a standalone factual statement (a "fact").
2. For each fact:
   - Determine whether it is likely **true** or **false/inaccurate** using:
     - Common knowledge
     - Logical reasoning
     - General world understanding
   - Mark:
     - `"is_true": true` — if the fact is clearly correct or plausible.
     - `"is_true": false` — if the fact is incorrect, misleading, implausible, or lacks factual basis.
   - Give a **concise, grounded reason** for your judgment using facts, common sense, or simple logic.

**Expected Output**:
Return only a **JSON list**, where each element has these fields:
- "fact": The sentence being evaluated
- "is_true": Boolean true/false
- "reason": Your justification

dont give triple quotes while giving out the json output, give only the json without any kind of brackets or quotes
Markdown content to analyze: 
\"\"\"{content}\"\"" 
"""
async def evaluate_accuracy(markdown: str):
    content = chunk_markdown(markdown)
    prompt = PROMPT_TEMPLATE.format(content=content)
    response = await gemini_flash(prompt)

    try:
        results = json.loads(response)
    except Exception as e:
        return f"❌ Failed to parse Gemini response as JSON:\n{response}\nError: {e}"

    total = len(results)
    correct = sum(1 for item in results if item.get("is_true") is True)
    score = round(correct / total, 2) if total > 0 else 0.0

    print("\n🔎 Accuracy Agent Output:")
    print(json.dumps(results, indent=2))
    print(f"\n✅ Calculated Accuracy Score: {correct}/{total} = {score}\n")

    return {
        "score": score,
        "total_facts": total,
        "correct_facts": correct,
        "details": results
    }
