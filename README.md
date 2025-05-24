# Semistructured Document Quality Analyzer

A modular Python framework for evaluating the quality of semistructured documents (like markdown files) across multiple dimensions using AI-powered agents.

## 📁 Project Structure

```
Engine/
│
├── agents/                       # All agents are LLM Calls with custom prompts
│   ├── accuracy_agent.py        # Evaluates factual accuracy of content
│   ├── completeness_agent.py    # Checks for missing information and gaps
│   ├── consistency_agent.py     # Verifies style and terminology consistency
│   ├── semanticoherence_agent.py # Assesses logical flow and connections
│   ├── timeliness_agent.py      # Checks data currency and relevance
│   └── uniqueness_agent.py      # Detects duplicate content
│
├── core/
│   ├── gemini_client.py        # Google Gemini API integration
│   └── markdown_utils.py       # Markdown text processing utilities
│
├── .env                        # Environment variables and API keys
├── evaluate.py                # Agent coordination and parallel execution
├── main.py                    # Entry point and result rendering
├── output.txt                 # Detailed evaluation results
├── requirements.txt           # Project dependencies
└── sample.md                  # Example markdown document for testing
```

## 🚀 Quick Start

1. **Setup Environment**
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure API Keys**
Create `.env` file:
```env
GOOGLE_API_KEY=your_api_key_here
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
```

3. **Run Analysis**
```bash
python main.py sample.md
```

## 📊 Quality Dimensions

1. **Accuracy**
   - Fact checking
   - Statement validation

2. **Completeness**
   - Missing information detection
   - Required context validation

3. **Consistency**
   - Style uniformity
   - Format adherence

4. **Semantic Coherence**
   - Logical flow
   - Topic transitions

5. **Timeliness**
   - Date validation
   - Reference recency

6. **Uniqueness**
   - Duplicate content detection
   - Redundancy checking
   - Content originality

## 🛠 Dependencies

- `httpx`: Async HTTP client for API calls
- `python-dotenv`: Environment configuration
- `google-generativeai`: Gemini LLM integration

## 📈 Output Format

Results are displayed in a structured format showing:
- Individual agent scores
- Detailed analysis per section
- Quality issues found
- Improvement suggestions
