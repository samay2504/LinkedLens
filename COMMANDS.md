# 🎯 Common Commands Reference

Quick reference for all common development tasks.

---

## 🐍 Backend Commands

### Setup & Installation
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov flake8 black mypy
```

### Running the Server
```bash
# Development server (auto-reload)
uvicorn api.main:app --reload

# Production server
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Custom port
uvicorn api.main:app --reload --port 8080

# With logging
uvicorn api.main:app --reload --log-level debug
```

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=api --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test function
pytest tests/test_api.py::test_health_check

# Run tests in parallel
pytest -n auto

# Watch mode (requires pytest-watch)
ptw
```

### Code Quality
```bash
# Linting
flake8 api

# Type checking
mypy api

# Format code
black api

# Check formatting without changes
black api --check

# Sort imports
isort api
```

### Environment Management
```bash
# Create .env from example
cp .env.example .env

# Show installed packages
pip list

# Show package info
pip show fastapi

# Update all packages
pip list --outdated
pip install -U package_name

# Freeze dependencies
pip freeze > requirements.txt
```

---

## 🎨 Frontend Commands

### Setup & Installation
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Install specific package
npm install axios

# Install dev dependency
npm install -D vite
```

### Running the Server
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Custom port
npm run dev -- --port 3000
```

### Package Management
```bash
# Check for outdated packages
npm outdated

# Update packages
npm update

# Update specific package
npm update axios

# Install and update package.json
npm install package@latest

# Remove package
npm uninstall package-name

# Clean install (delete node_modules first)
rm -rf node_modules package-lock.json
npm install
```

---

## 🚢 Deployment Commands

### Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# Environment variables
vercel env add VARIABLE_NAME
vercel env ls
vercel env rm VARIABLE_NAME
```

### Docker (Optional)
```bash
# Build backend image
docker build -t linkedin-post-backend ./backend

# Run backend container
docker run -p 8000:8000 --env-file backend/.env linkedin-post-backend

# Build frontend image
docker build -t linkedin-post-frontend ./frontend

# Run frontend container
docker run -p 5173:5173 linkedin-post-frontend

# Docker Compose (if configured)
docker-compose up
docker-compose down
```

---

## 🔍 Git Commands

### Basic Workflow
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "feat: add new feature"

# Push to remote
git push origin main

# Pull from remote
git pull origin main

# Create new branch
git checkout -b feature/new-feature

# Switch branch
git checkout main

# Merge branch
git merge feature/new-feature
```

### Useful Git Commands
```bash
# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Stash changes
git stash
git stash pop

# View remotes
git remote -v

# Add remote
git remote add origin https://github.com/user/repo.git
```

---

## 🧪 Testing & Debugging

### API Testing with cURL
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Generate post
curl -X POST http://localhost:8000/api/v1/generate-post \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence"}'

# With pretty JSON output
curl http://localhost:8000/api/v1/health | jq
```

### API Testing with httpie (if installed)
```bash
# Install httpie
pip install httpie

# Health check
http GET http://localhost:8000/api/v1/health

# Generate post
http POST http://localhost:8000/api/v1/generate-post topic="AI"
```

### View Logs
```bash
# Backend logs (if file logging configured)
tail -f backend/logs/app.log

# Follow logs in real-time
tail -f backend/logs/app.log | grep ERROR

# Vercel logs
vercel logs [deployment-url]
```

---

## 🔧 Troubleshooting Commands

### Python Issues
```bash
# Check Python version
python --version

# Check pip version
pip --version

# Upgrade pip
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Reinstall package
pip uninstall package-name
pip install package-name
```

### Node.js Issues
```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# Clear npm cache
npm cache clean --force

# Verify npm
npm cache verify

# Update npm
npm install -g npm@latest
```

### Port Issues
```bash
# Check what's using port 8000 (Windows)
netstat -ano | findstr :8000

# Check what's using port 8000 (macOS/Linux)
lsof -i :8000

# Kill process on port (Windows)
taskkill /PID <PID> /F

# Kill process on port (macOS/Linux)
kill -9 <PID>
```

### Database/Cache (if using)
```bash
# Redis CLI
redis-cli

# Flush Redis cache
redis-cli FLUSHALL

# PostgreSQL
psql -U username -d database_name

# Check PostgreSQL connection
psql -U username -h localhost -p 5432 -d database_name
```

---

## 📊 Performance & Monitoring

### Backend Performance
```bash
# Profile Python code
python -m cProfile -o output.prof api/main.py

# Memory profiling
pip install memory_profiler
python -m memory_profiler api/main.py

# Load testing with locust
pip install locust
locust -f locustfile.py
```

### Frontend Performance
```bash
# Build size analysis
npm run build -- --analyze

# Lighthouse audit
npm install -g lighthouse
lighthouse http://localhost:5173
```

---

## 🔄 CI/CD Commands

### GitHub Actions
```bash
# Trigger workflow manually (from GitHub CLI)
gh workflow run backend-ci.yml

# View workflow runs
gh run list

# View workflow logs
gh run view [run-id]
```

---

## 📦 Package Scripts

### Backend (if using Makefile)
```bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run server
make run
```

### Frontend (custom npm scripts)
```bash
# Add to package.json scripts section:
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "lint": "eslint src --ext .vue,.js",
  "format": "prettier --write src/"
}
```

---

## 🎓 Learning Commands

### Python REPL Testing
```bash
# Start Python shell with environment
cd backend
source venv/bin/activate
python

# In Python shell:
>>> from api.services.langchain_agent import NewsToLinkedInAgent
>>> agent = NewsToLinkedInAgent(api_key="test")
>>> # Test methods here
```

### Node.js REPL Testing
```bash
# Start Node.js shell
node

# In Node.js shell:
> const axios = require('axios');
> axios.get('http://localhost:8000/api/v1/health')
>   .then(res => console.log(res.data));
```

---

## 🎯 Quick Reference

### Start Development
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && uvicorn api.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Run Tests
```bash
# Backend
cd backend && pytest -v

# Frontend
cd frontend && npm run build
```

### Deploy
```bash
# Backend
cd backend && vercel --prod

# Frontend
cd frontend && vercel --prod
```

---

## 📝 Notes

- Replace `source venv/bin/activate` with `.\venv\Scripts\activate` on Windows
- Use `python3` instead of `python` on some systems
- Add `sudo` prefix on Linux/macOS if permission denied
- Check `.env` files are properly configured before running

---

**Tip**: Bookmark this file for quick reference! 🔖
