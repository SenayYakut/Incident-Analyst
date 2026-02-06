# Autonomous Incident Analyst

A stateful AI agent that analyzes system logs, retrieves similar past incidents, suggests fixes, and updates its internal memory.

## Features

- **Stateful Reasoning**: Maintains context across interactions
- **Incident Memory**: Retrieves similar past incidents for better recommendations
- **Autonomous Analysis**: Suggests root causes and fixes based on log patterns
- **Iterative Improvement**: Updates recommendations based on attempted fixes

## Tech Stack

- **Frontend**: Next.js
- **Backend**: FastAPI (Python)
- **LLM**: You.com API
- **Deployment**: Render

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /incident` - Submit logs for analysis
- `POST /action` - Apply suggested fixes
- `POST /resolve` - Mark incident as resolved

## Built for Continual Learning Hackathon 2025
