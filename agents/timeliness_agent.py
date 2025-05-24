import json
from core.gemini_client import gemini_flash

PROMPT_TEMPLATE = """
You are a world-class data quality expert with deep expertise in content evaluation and prompt design. Your task is to assess the **timeliness** of the provided markdown content.

**Definition**:
Timeliness refers to whether the content is **current, relevant to the present time**, and **free from outdated or expired information**. A statement is considered **timely** if it:
- Contains references to current events, data, or conditions that are still valid.
- Avoids mentioning outdated products, policies, statistics, technologies, or news unless clearly contextualized as historical.
- Reflects awareness of the present timeline (e.g., not stating that an event "will happen" if it already occurred).

**Instructions**:
1. Carefully examine each sentence or block for **explicit or implicit time references**.
2. For each time-aware statement:
   - Determine whether the information is **still accurate and relevant as of today**.
   - Use general knowledge, public events, or logical reasoning to judge timeliness.
   - Flag content that refers to outdated technologies, discontinued events, expired timelines, or past forecasts stated in future tense.
3. For each checkable unit, return:
   - `"unit"`: The specific sentence or paragraph containing a time reference.
   - `"is_timely"`: true if the unit is still current and relevant, false otherwise.
   - `"issue"`: A short explanation if it’s outdated, expired, or misleading due to time-sensitive phrasing.

**Expected Output**:
Return only a **JSON list**, where each element has:
- "unit": The sentence or paragraph evaluated
- "is_timely": Boolean true/false
- "issue": Brief explanation or `null` if none

Do not use triple quotes to wrap the JSON output.

Markdown content to analyze:
\"\"\"{content}\"\"\"
"""

async def evaluate_timeliness(markdown: str):
    prompt = PROMPT_TEMPLATE.format(content=markdown)
    response = await gemini_flash(prompt)

    try:
        results = json.loads(response)
    except Exception as e:
        return f"❌ Failed to parse Gemini response as JSON:\n{response}\nError: {e}"

    total = len(results)
    outdated = sum(1 for item in results if item.get("is_timely") is False)
    score = round(1 - (outdated / total), 2) if total > 0 else 0.0

    print("\n🔎 Timeliness Agent Output:")
    print(json.dumps(results, indent=2))
    print(f"\n✅ Calculated Timeliness Score: 1 - ({outdated}/{total}) = {score}\n")

    return {
        "score": score,
        "total_units": total,
        "timely_units": total - outdated,
        "outdated_units": outdated,
        "details": results
    }
