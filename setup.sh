#!/bin/bash

# Setup script for Autonomous Incident Analyst
# Initializes environment files and dependencies

set -e

echo "🚀 Autonomous Incident Analyst - Setup Script"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 20 or higher."
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node ${NODE_VERSION} found${NC}"

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

NPM_VERSION=$(npm --version)
echo -e "${GREEN}✓ npm ${NPM_VERSION} found${NC}"

echo ""

# Setup backend
echo -e "${BLUE}📦 Setting up backend...${NC}"

cd backend

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
    echo -e "${YELLOW}⚠  Please edit backend/.env and add your YOU_API_KEY${NC}"
    echo -e "${YELLOW}   Get your key at: https://you.com/api${NC}"
else
    echo -e "${GREEN}✓ backend/.env already exists${NC}"
fi

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

echo "Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Python dependencies installed${NC}"

cd ..

# Setup frontend
echo ""
echo -e "${BLUE}📦 Setting up frontend...${NC}"

cd frontend

if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo -e "${GREEN}✓ Created frontend/.env.local${NC}"
else
    echo -e "${GREEN}✓ frontend/.env.local already exists${NC}"
fi

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install --silent
    echo -e "${GREEN}✓ Node dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Node dependencies already installed${NC}"
fi

cd ..

# Make scripts executable
echo ""
echo -e "${BLUE}🔧 Setting up scripts...${NC}"
chmod +x start-local.sh
chmod +x test-api.sh
chmod +x setup.sh
echo -e "${GREEN}✓ Scripts are now executable${NC}"

# Summary
echo ""
echo "=============================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo "=============================================="
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Configure your API key (optional but recommended):"
echo "   Edit backend/.env and add your YOU_API_KEY"
echo "   Get one at: https://you.com/api"
echo ""
echo "2. Start the application:"
echo "   Option A - Docker Compose:"
echo "     docker-compose up"
echo ""
echo "   Option B - Local Development:"
echo "     ./start-local.sh"
echo ""
echo "   Option C - Manual Start:"
echo "     Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "     Terminal 2: cd frontend && npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "4. Test the API:"
echo "   ./test-api.sh"
echo ""
echo -e "${YELLOW}💡 Tip: The system works without an API key using pattern matching,${NC}"
echo -e "${YELLOW}   but adding a You.com API key enables advanced LLM analysis.${NC}"
echo ""
