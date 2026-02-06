# 🚀 Quick Start Guide

Get up and running with Autonomous Incident Analyst in minutes!

## ⚡ Fastest Way (Docker Compose)

```bash
# Start everything
docker-compose up -d

# Access the app
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🛠️ Local Development

```bash
# One-command setup
./setup.sh

# Start services
./start-local.sh

# Test the API
./test-api.sh
```

## 📝 Manual Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Optional: Add API Key

```bash
# Edit backend/.env
YOU_API_KEY=your_key_here
```

Get your key at: https://you.com/api

**Note**: Works without API key using pattern matching!

## 🧪 Test the API

```bash
./test-api.sh
```

Or manually:
```bash
curl http://localhost:8000/health | jq
```

## 📚 Full Documentation

- **Complete Guide**: [README.md](README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Changes**: [CHANGELOG.md](CHANGELOG.md)
- **Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 🎯 Example Usage

### 1. Submit an Incident
```bash
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] Container OOMKilled\n[ERROR] Memory exceeded",
    "metrics": "Memory: 512Mi/512Mi"
  }'
```

### 2. View Response
- Root causes identified
- Suggested fix provided
- Similar past incidents shown
- Confidence level indicated

### 3. Apply Fix
```bash
curl -X POST http://localhost:8000/action \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 1,
    "fix_applied": "Increased memory to 1Gi"
  }'
```

### 4. Resolve
```bash
curl -X POST http://localhost:8000/resolve \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 1,
    "resolution_notes": "Memory optimized"
  }'
```

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Web UI |
| Backend | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | API Reference |
| Health | http://localhost:8000/health | System Status |

## 🎨 Features

✅ AI-powered log analysis  
✅ Pattern matching fallback  
✅ Incident memory & learning  
✅ Similarity search (RAG)  
✅ Confidence scoring  
✅ Iterative problem solving  
✅ Beautiful modern UI  

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill
lsof -ti:3000 | xargs kill
```

**Dependencies issue?**
```bash
# Re-run setup
./setup.sh
```

**Need help?**
- Check [README.md](README.md)
- Open an issue on GitHub
- Review logs: `docker-compose logs`

## 📊 Health Check

```bash
curl http://localhost:8000/health | jq
```

Response shows:
- System status
- Component health
- Incident statistics
- Available features

## 🎓 Learn More

This project demonstrates:
- Stateful AI agents
- Retrieval-Augmented Generation (RAG)
- Continuous learning
- Incident management workflows

Built for **Continual Learning Hackathon 2025**

## 💡 Pro Tips

1. **No API key needed** - Works great with pattern matching
2. **Docker is easiest** - Use `docker-compose up -d`
3. **Test script validates** - Run `./test-api.sh` to verify
4. **Health endpoint monitors** - Check `/health` for stats
5. **Memory builds up** - More incidents = better analysis

## 🚦 Status

Project Status: **Production Ready** ✅

- ✅ Backend operational
- ✅ Frontend builds
- ✅ Tests passing
- ✅ Docker working
- ✅ Documentation complete
- ✅ Deployment ready

---

**Need the full story?** → [README.md](README.md)  
**Want to contribute?** → [CONTRIBUTING.md](CONTRIBUTING.md)  
**See what's new?** → [CHANGELOG.md](CHANGELOG.md)
