import json
from core.gemini_client import gemini_flash

PROMPT_TEMPLATE = """
You are a world-class data quality expert specializing in assessing **completeness** of markdown content. Your job is to rigorously evaluate whether the information presented is thorough, sufficiently detailed, and not missing critical components.

**Definition**:
Completeness refers to the extent to which all required or expected information is present in the content. Complete content contains:
- Full and coherent sentences that make sense on their own.
- Adequate detail to understand a topic, with no obvious gaps.
- All expected fields or sections for a given context (e.g., missing definitions, broken lists, empty bullet points).
- Logical flow and continuity across paragraphs.
- Sufficient **information density** to ensure the content is useful and self-contained.

**Instructions**:
1. You will receive the markdown content in full.
2. Evaluate each **logical block or paragraph** as a unit of analysis.
3. For each block, determine:
   - Is the information presented **complete**? Does it feel like something is missing or left unsaid?
   - Are there unfinished thoughts, empty sections, missing headings, or unexplained items?

**Expected Output**:
Return only a **JSON list**, where each element has the following fields:
- "section": A paragraph or block of text from the markdown.
- "is_complete": Boolean true/false — whether the section appears complete.
- "missing_info": A concise explanation of what is missing or why the section is considered incomplete (e.g., "lacks examples", "ends abruptly", "missing explanation of X").

dont give triple quotes while giving out the json output

Markdown content to analyze:
\"\"\"{content}\"\"\"
"""

async def evaluate_completeness(markdown: str):
    prompt = PROMPT_TEMPLATE.format(content=markdown)
    response = await gemini_flash(prompt)

    try:
        results = json.loads(response)
    except Exception as e:
        return f"❌ Failed to parse Gemini response as JSON:\n{response}\nError: {e}"

    total = len(results)
    incomplete = sum(1 for item in results if item.get("is_complete") is False)
    score = round(1 - (incomplete / total), 2) if total > 0 else 0.0

    print("\n🔎 Completeness Agent Output:")
    print(json.dumps(results, indent=2))
    print(f"\n✅ Calculated Completeness Score: 1 - ({incomplete}/{total}) = {score}\n")

    return {
        "score": score,
        "total_sections": total,
        "complete_sections": total - incomplete,
        "incomplete_sections": incomplete,
        "details": results
    }
