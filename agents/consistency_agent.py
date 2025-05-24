import json
from core.gemini_client import gemini_flash

PROMPT_TEMPLATE = """
You are a world-class data quality expert specializing in linguistic, stylistic, and structural consistency. Your task is to evaluate the **consistency** of the provided markdown content.

**Definition**:
Consistency refers to the internal uniformity of the content in terms of:
- Terminology: consistent use of terms, variable names, and technical vocabulary.
- Formatting: uniform use of bullet points, headings, code blocks, etc.
- Tone & Style: similar narrative voice, formality, or writing style throughout.
- Structure: stable document layout and coherent progression of ideas.
Inconsistencies may include changes in style, formatting errors, term drift, or abrupt shifts in tone.

**Instructions**:
1. Carefully analyze the markdown content holistically and at the block/paragraph level.
2. For each identified **checkable unit** (paragraph, section, or formatting cluster), determine:
   - Is this unit consistent with the rest of the document in style, terminology, tone, and formatting?
3. For each unit, return the following fields:
   - `"unit"`: the specific content being checked (e.g., a paragraph or section)
   - `"is_consistent"`: true if it’s consistent, false otherwise
   - `"issue"`: A brief explanation of what inconsistency was found (e.g., "title case mismatch", "sudden change in tone", "italic formatting breaks", etc.)

**Expected Output**:
Only return a **JSON list** with each item having:
- "unit": The portion of content being evaluated
- "is_consistent": Boolean true/false
- "issue": Short description of inconsistency or `null` if none

dont give triple quotes while giving out the json output, give only the json without any kind of brackets or quotes

Markdown content to analyze:
\"\"\"{content}\"\"\"
"""

async def evaluate_consistency(markdown: str):
    prompt = PROMPT_TEMPLATE.format(content=markdown)
    response = await gemini_flash(prompt)

    try:
        results = json.loads(response)
    except Exception as e:
        return f"❌ Failed to parse Gemini response as JSON:\n{response}\nError: {e}"

    total = len(results)
    inconsistent = sum(1 for item in results if item.get("is_consistent") is False)
    score = round(1 - (inconsistent / total), 2) if total > 0 else 0.0

    print("\n🔎 Consistency Agent Output:")
    print(json.dumps(results, indent=2))
    print(f"\n✅ Calculated Consistency Score: 1 - ({inconsistent}/{total}) = {score}\n")

    return {
        "score": score,
        "total_units": total,
        "consistent_units": total - inconsistent,
        "inconsistent_units": inconsistent,
        "details": results
    }
