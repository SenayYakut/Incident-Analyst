# Autonomous Incident Analyst

A stateful AI agent that analyzes system logs, retrieves similar past incidents, suggests fixes, and updates its internal memory.

## Features

- **Stateful Reasoning**: Maintains context across interactions
- **Incident Memory**: Retrieves similar past incidents for better recommendations
- **Autonomous Analysis**: Suggests root causes and fixes based on log patterns
- **Iterative Improvement**: Updates recommendations based on attempted fixes
- **Pattern Matching**: Intelligent fallback analysis when LLM API is unavailable
- **Similarity Search**: RAG-like retrieval of past resolved incidents

## Tech Stack

- **Frontend**: Next.js 14 with TypeScript
- **Backend**: FastAPI (Python 3.11+)
- **LLM**: You.com API (with intelligent fallback)
- **Deployment**: Render (with Docker support)
- **Storage**: JSON-based incident memory

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend   │─────▶│  You.com    │
│  (Next.js)  │◀─────│  (FastAPI)  │◀─────│  LLM API    │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  Incident   │
                     │   Memory    │
                     │ (JSON Store)│
                     └─────────────┘
```

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd autonomous-incident-analyst

# Set up environment variables (optional)
cp backend/.env.example backend/.env
# Edit backend/.env and add your YOU_API_KEY if available

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Prerequisites
- Python 3.11+
- Node.js 20+
- npm or yarn

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment (optional)
cp .env.example .env
# Edit .env and add your YOU_API_KEY

# Start the server
uvicorn main:app --reload --port 8000

# Or run directly
python main.py
```

Backend will be available at http://localhost:8000

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local if needed (default: http://localhost:8000)

# Start development server
npm run dev

# Or build for production
npm run build
npm start
```

Frontend will be available at http://localhost:3000

### Option 3: Quick Start Script

```bash
# Make the script executable
chmod +x start-local.sh

# Run the script
./start-local.sh
```

This will automatically set up and start both backend and frontend services.

## API Endpoints

### Core Endpoints

- `GET /` - Health check
- `GET /incidents` - List all incidents
- `GET /incidents/{id}` - Get specific incident
- `POST /incident` - Submit logs for analysis
- `POST /action` - Apply suggested fixes
- `POST /resolve` - Mark incident as resolved
- `DELETE /incidents/{id}` - Delete incident (for testing)

### API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Automated API Testing

Run the test script to verify all endpoints:

```bash
# Make sure backend is running first
./test-api.sh

# Or specify a different API URL
API_URL=https://your-api.com ./test-api.sh
```

### Manual Testing Examples

#### Submit an Incident

```bash
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] 2024-02-06 10:23:45 - Container killed: OOMKilled\n[ERROR] Memory usage exceeded limit: 512Mi",
    "metrics": "Memory: 512Mi/512Mi (100%)\nCPU: 85%"
  }'
```

#### Apply a Fix

```bash
curl -X POST http://localhost:8000/action \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 1,
    "fix_applied": "Increased memory limit to 1Gi",
    "new_logs": "[INFO] Container running normally"
  }'
```

#### Resolve an Incident

```bash
curl -X POST http://localhost:8000/resolve \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 1,
    "resolution_notes": "Memory limit increased and application optimized"
  }'
```

## Configuration

### Backend Environment Variables

- `YOU_API_KEY` - Your You.com API key (get it at https://you.com/api)
  - Optional: System will use intelligent pattern matching if not provided
  - Recommended for best results

### Frontend Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Deployment

### Deploy to Render

1. Fork/clone this repository
2. Connect your GitHub repo to Render
3. Render will automatically detect `render.yaml` and deploy both services
4. Add `YOU_API_KEY` as an environment variable in Render dashboard
5. Services will be available at the URLs provided by Render

### Docker Deployment

```bash
# Build images
docker-compose build

# Run in production mode
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## How It Works

### 1. Incident Submission
User submits logs and metrics → Backend creates incident record → System searches for similar past incidents

### 2. AI Analysis
- Searches incident memory for similar resolved incidents
- Sends context to You.com LLM for analysis
- Falls back to pattern matching if LLM unavailable
- Returns suspected root causes and suggested fixes

### 3. Iterative Resolution
- User applies suggested fixes
- System re-evaluates incident state
- Provides updated recommendations
- Tracks all attempted fixes

### 4. Memory Update
- Resolved incidents stored with resolution notes
- Used as context for future similar incidents
- Implements basic RAG (Retrieval-Augmented Generation)

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── llm.py               # LLM integration
│   ├── memory.py            # Incident storage/retrieval
│   ├── incidents.json       # Incident database
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── .env.example        # Environment template
├── frontend/
│   ├── app/
│   │   ├── page.tsx        # Main UI component
│   │   ├── layout.tsx      # App layout
│   │   └── globals.css     # Styles
│   ├── package.json        # Node dependencies
│   ├── Dockerfile          # Frontend container
│   └── .env.example        # Environment template
├── docker-compose.yml       # Local development setup
├── render.yaml             # Render deployment config
├── test-api.sh             # API testing script
├── start-local.sh          # Quick start script
└── README.md               # This file
```

## Features in Detail

### Stateful Memory
- Stores all incidents, fixes, and resolutions
- Calculates similarity between incidents using string matching
- Retrieves top-k similar resolved incidents for context

### Pattern Matching Fallback
When LLM API is unavailable, the system uses pattern matching for:
- OOM (Out of Memory) errors
- Connection refused errors
- Timeout issues
- Permission denied errors
- Disk space issues
- And more...

### Confidence Scoring
- High: Clear error pattern with known solutions
- Medium: Ambiguous symptoms or multiple possible causes
- Low: Unknown pattern requiring manual investigation

## Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed
- Check all dependencies are installed: `pip install -r backend/requirements.txt`
- Verify port 8000 is not in use

### Frontend won't start
- Ensure Node.js 20+ is installed
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Verify port 3000 is not in use

### CORS errors
- Ensure backend is running on http://localhost:8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Backend CORS is configured to allow all origins (adjust in production)

### LLM not working
- Verify `YOU_API_KEY` is set correctly
- Check You.com API status and quota
- System will automatically fall back to pattern matching

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - feel free to use this project for learning and development.

## Built for Continual Learning Hackathon 2025

This project demonstrates:
- Stateful AI agents with memory
- Retrieval-Augmented Generation (RAG) patterns
- Continuous learning from past incidents
- Iterative problem-solving workflows
- Graceful degradation with intelligent fallbacks
