# AI Jira Backend (Backend Developer 2)

## Setup
1. Create virtual environment  
   `python -m venv .venv`  
   `.\.venv\Scripts\activate`
2. Install dependencies  
   `pip install -r requirements.txt`

## Run
`python src/app.py`

## Test
`pytest`

## API Endpoints
- GET `/health` → returns status
- POST `/generate` → generates stories/test cases
- GET `/runs/<run_id>/json`
- GET `/runs/<run_id>/csv`
