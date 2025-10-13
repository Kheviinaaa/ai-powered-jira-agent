AI Engineer 1 – Setup & Run Guide
=================================

1) Open PowerShell or VS Code Terminal in this folder:
   C:\Users\Eshna\Documents\ai_agent_project

   (If using VS Code)
   - Open the project folder in VS Code
   - Go to Terminal → “New Terminal”
   - Ensure you see (.venv) when the environment is activated

2) Create and activate a virtual environment:
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Mac/Linux

3) Install dependencies:
   pip install -r requirements.txt

4) (Optional) Set your OpenAI API key
   If you have an API key, run:
       setx OPENAI_API_KEY "your_api_key_here"   # Windows
       export OPENAI_API_KEY="your_api_key_here" # Mac/Linux
   If no key is set, the program will automatically use mock data.

5) Run the AI Engine:
   python src\ai_engine.py

6) Outputs will appear in:
   out\sample_output.json        ← generated user stories & test cases
   out\validation_report.json    ← validation summary

7) Run automated tests (for Test Engineer):
   python -m pytest tests\test_ai_engine.py

Folder Structure
----------------
- src/         → main AI logic, prompts, schemas
- mock_data/   → sample epics for testing
- out/         → generated results (JSON)
- tests/       → simple validation tests
