#!/bin/bash

# AI-Powered LinkedIn Post Generator Setup Script
# For macOS and Linux

echo "========================================"
echo "  LinkedIn Post Generator Setup"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Check Node.js installation
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Backend Setup${NC}"
echo -e "${CYAN}========================================${NC}"

# Navigate to backend
cd backend

# Create virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env and add your GEMINI_API_KEY${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete!${NC}"

# Navigate back and to frontend
cd ..
echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Frontend Setup${NC}"
echo -e "${CYAN}========================================${NC}"

cd frontend

# Install Node.js dependencies
echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
npm install

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
fi

echo -e "${GREEN}✓ Frontend setup complete!${NC}"

# Navigate back
cd ..

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Setup Complete! 🎉${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit backend/.env and add your GEMINI_API_KEY"
echo "   Get it from: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn api.main:app --reload"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo -e "${CYAN}Happy coding! 🚀${NC}"
