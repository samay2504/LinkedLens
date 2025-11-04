# ⚡ Quick Start Guide

Get the LinkedIn Post Generator running in 5 minutes!

## 🎯 Prerequisites

Before starting, make sure you have:

- ✅ **Python 3.11+** ([Download](https://www.python.org/downloads/))
- ✅ **Node.js 18+** ([Download](https://nodejs.org/))
- ✅ **Google Gemini API Key** ([Get it free](https://makersuite.google.com/app/apikey))

## 🚀 Automated Setup (Recommended)

### Windows (PowerShell)

```powershell
# Run setup script
.\setup.ps1
```

### macOS / Linux

```bash
# Make script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

The script will:
1. Check Python and Node.js installations
2. Set up Python virtual environment
3. Install all backend dependencies
4. Install all frontend dependencies
5. Create `.env` files from examples

## 🔑 Configure API Key

After running the setup script:

1. Open `backend/.env` in your text editor
2. Replace `your_gemini_api_key_here` with your actual API key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_actual_key
   ```
3. Save the file

## ▶️ Start the Application

### Terminal 1: Backend

```bash
# Navigate to backend
cd backend

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start backend server
uvicorn api.main:app --reload
```

Backend runs at: http://localhost:8000  
API Docs: http://localhost:8000/docs

### Terminal 2: Frontend

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Start development server
npm run dev
```

Frontend runs at: http://localhost:5173

## ✨ Test the Application

1. Open http://localhost:5173 in your browser
2. Enter a topic (e.g., "Artificial Intelligence")
3. Click "GENERATE POST"
4. Wait 10-20 seconds for AI to generate content
5. Copy the generated LinkedIn post!

## 📱 What You'll See

```
┌─────────────────────────────────────┐
│  THE LINKEDIN POST GENERATOR        │
│  AI-Powered News to Professional    │
│  Content                            │
├─────────────────────────────────────┤
│                                     │
│  TOPIC                              │
│  [Enter topic here...]              │
│  [GENERATE POST]                    │
│                                     │
├─────────────────────────────────────┤
│  Generated LinkedIn Post            │
│  [Copy to Clipboard]                │
│                                     │
│  🤖 Your AI-generated post here...  │
│                                     │
│  Topic: [Your topic]                │
│  News Sources: [Links...]           │
│  Suggested Image: [Description]     │
└─────────────────────────────────────┘
```

## 🐛 Troubleshooting

### "uvicorn: command not found"

Make sure virtual environment is activated:
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### "Module not found" errors

Reinstall dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### "npm: command not found"

Install Node.js from [nodejs.org](https://nodejs.org/)

### "API Key error"

1. Verify your API key is correct in `backend/.env`
2. Check that the API is enabled in Google Cloud Console
3. Ensure billing is set up (free tier available)

### "CORS error" in browser

1. Make sure backend is running on port 8000
2. Check `CORS_ORIGINS` in `backend/.env`
3. Restart both servers

### Frontend can't connect to backend

1. Verify backend is running at http://localhost:8000
2. Check `VITE_API_URL` in `frontend/.env`
3. Try opening http://localhost:8000/api/v1/health

## 📚 Next Steps

- ✅ **Explore API Docs**: http://localhost:8000/docs
- ✅ **Read Full README**: [README.md](README.md)
- ✅ **Deploy to Vercel**: [DEPLOYMENT.md](DEPLOYMENT.md)
- ✅ **Run Tests**: `cd backend && pytest tests/ -v`
- ✅ **Customize UI**: Edit `frontend/src/style.css`

## 🎥 Video Tutorial

Watch the 2-3 minute explanation video (when available): [Link to be added]

## 💡 Pro Tips

1. **Faster Development**: Use `--reload` flag with uvicorn (already included)
2. **View Logs**: Check `backend/logs/` for detailed logs
3. **Test API**: Use Swagger UI at `/docs` to test endpoints
4. **Hot Reload**: Both frontend and backend auto-reload on changes
5. **Clear Cache**: If issues persist, delete `__pycache__` and `node_modules`

## 🆘 Still Stuck?

1. Check the main [README.md](README.md) for detailed documentation
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
3. Check [DELIVERABLES_CHECKLIST.md](DELIVERABLES_CHECKLIST.md) for completeness
4. Open an issue on GitHub (if repository is public)

## ⏱️ Expected Generation Time

- First request: 15-25 seconds (cold start)
- Subsequent requests: 10-15 seconds
- With caching (future): 1-3 seconds

## 🎉 Success!

If you see the generated LinkedIn post, congratulations! You've successfully set up the AI-Powered LinkedIn Post Generator.

Now you can:
- Generate unlimited LinkedIn posts
- Customize the prompts in `backend/api/services/langchain_agent.py`
- Modify the UI theme in `frontend/src/style.css`
- Deploy to production using Vercel

Happy posting! 🚀

---

**Time to Complete**: 5-10 minutes  
**Difficulty**: Easy  
**Cost**: Free (with Gemini API free tier)
