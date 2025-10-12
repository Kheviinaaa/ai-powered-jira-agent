AI Engineer 1 – Setup & Run Guide

1) Open PowerShell in this folder:
   C:\Users\Eshna\Documents\ai_agent_project

2) Install dependencies:
   pip install -r requirements.txt

3) Set your OpenAI API key (optional, fallback works without it):
   setx OPENAI_API_KEY "your_api_key_here"

4) Run the engine:
   python src\ai_engine.py

5) Outputs will appear in:
   out\sample_output.json
   out\validation_report.json

Folders:
- src/        → main AI logic, prompts, schemas
- mock_data/  → sample epics for testing
- out/        → generated results
- tests/      → simple validation tests
