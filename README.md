# 🤖 AI-Powered LinkedIn Post Generator

[![Backend CI/CD](https://github.com/yourusername/linkedin-post-generator/workflows/Backend%20CI/CD/badge.svg)](https://github.com/yourusername/linkedin-post-generator/actions)
[![Frontend CI/CD](https://github.com/yourusername/linkedin-post-generator/workflows/Frontend%20CI/CD/badge.svg)](https://github.com/yourusername/linkedin-post-generator/actions)

> Transform any topic into engaging LinkedIn content powered by Google Gemini AI and LangChain

## 📦 Deliverables

✅ **GitHub Repository**: Clean commit history with comprehensive documentation  
✅ **Hosted API**: Deployed on Vercel with Swagger documentation  
✅ **Voice Recording**: 2-3 minute explanation of the project (see [VOICE_RECORDING_SCRIPT.md](VOICE_RECORDING_SCRIPT.md))

**Live Links:**
- 🌐 **Hosted Swagger API**: [https://your-backend.vercel.app/docs](https://your-backend.vercel.app/docs)
- 🎨 **Frontend Demo**: [https://your-frontend.vercel.app](https://your-frontend.vercel.app)
- 🎙️ **Voice Recording**: [Link to recording]

## 🎯 Project Requirements ✅

### ✅ 1. AI + LangChain Agent
- **Google Gemini API** integration with free account support
- **LangChain ReAct Agent** with web access via search tools
- **Multi-engine search**: Google → Yahoo → DuckDuckGo fallback
- **Groq API** as fallback LLM provider for reliability
- **Features**:
  - ✅ Searches for recent news/articles on any topic
  - ✅ Generates professional + engaging LinkedIn posts
  - ✅ British English style (no asterisks, proper formatting)
  - ✅ Includes image suggestions

### ✅ 2. Backend (FastAPI)
- **Endpoint**: `POST /api/v1/generate-post`
- **Input**: `{"topic": "Artificial Intelligence"}`
- **Output**: 
  ```json
  {
    "topic": "Artificial Intelligence",
    "news_sources": ["url1", "url2", "url3"],
    "linkedin_post": "AI is transforming industries... [generated text]",
    "image_suggestion": "Optional image URL or null",
    "generated_at": "2025-11-05T10:30:00"
  }
  ```
- **Swagger Documentation**: Auto-generated at `/docs` endpoint
- **Additional Features**:
  - Health check endpoint at `/api/v1/health`
  - Structured logging with Structlog
  - Comprehensive error handling
  - Production-ready with 72% test coverage

### ✅ 3. Deployment
- **Platform**: Vercel (serverless functions)
- **Swagger Link**: Available at `https://your-backend.vercel.app/docs`
- **Environment Variables**: Configured via Vercel CLI
- **CI/CD**: GitHub Actions for automated testing and deployment
- **See**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions

### ✅ 4. Voice Explanation
- **Script Prepared**: See [VOICE_RECORDING_SCRIPT.md](VOICE_RECORDING_SCRIPT.md)
- **Content Covers**:
  - What was built (architecture, features)
  - How to improve (auth, rate limiting, caching, async processing)
  - Production scaling (PostgreSQL, Redis, Celery, monitoring)
  - Database design for thousands of users

## 🌟 Features

- 🤖 **AI-Powered Generation**: Uses Google Gemini Pro for intelligent content creation
- 🔍 **Real-Time News Search**: Fetches latest news using DuckDuckGo integration
- 📝 **Professional Content**: Creates LinkedIn-optimized posts with hooks and CTAs
- 🎨 **Newspaper Theme UI**: Clean, minimalist design inspired by classic newspapers
- 🚀 **Production Ready**: Comprehensive logging, error handling, and monitoring
- ☁️ **Vercel Deployment**: One-click deployment for both frontend and backend
- 🧪 **Fully Tested**: Unit tests with pytest and comprehensive test coverage
- 📊 **API Documentation**: Auto-generated Swagger and ReDoc documentation

## 📸 Demo

![LinkedIn Post Generator](docs/screenshot.png)

**Live Demo**: [https://your-app.vercel.app](https://your-app.vercel.app)  
**API Docs**: [https://your-api.vercel.app/docs](https://your-api.vercel.app/docs)

## 🏗️ Architecture

```
┌─────────────────┐      HTTP      ┌─────────────────┐
│                 │──────────────→  │                 │
│   Vue.js 3      │                 │   FastAPI       │
│   Frontend      │  ←──────────────│   Backend       │
│                 │     JSON        │                 │
└─────────────────┘                 └────────┬────────┘
                                             │
                                             ↓
                                    ┌────────────────┐
                                    │ Google Gemini  │
                                    │   + LangChain  │
                                    └────────┬───────┘
                                             │
                                             ↓
                                    ┌────────────────┐
                                    │  DuckDuckGo    │
                                    │  News Search   │
                                    └────────────────┘
```

### Technology Stack

**Frontend**
- Vue.js 3 (Composition API)
- Vite (Build tool)
- Axios (HTTP client)
- Pure CSS (Newspaper theme)

**Backend**
- FastAPI (Python 3.11+)
- Google Gemini API (gemini-pro)
- LangChain (AI orchestration)
- DuckDuckGo Search (News retrieval)
- Structlog (Advanced logging)
- Pydantic v2 (Validation)

**DevOps**
- Vercel (Deployment)
- GitHub Actions (CI/CD)
- pytest (Testing)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your GEMINI_API_KEY
# GEMINI_API_KEY=your_actual_api_key_here

# Run development server
uvicorn api.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`  
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Edit .env if needed
# VITE_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 📖 API Usage

### Generate LinkedIn Post

**Endpoint:** `POST /api/v1/generate-post`

**Request Body:**
```json
{
  "topic": "Artificial Intelligence"
}
```

**Response:**
```json
{
  "topic": "Artificial Intelligence",
  "news_sources": ["url1", "url2", "url3"],
  "linkedin_post": "AI is transforming industries... [generated text]",
  "image_suggestion": "Optional image URL or null",
  "generated_at": "2025-11-05T10:30:00"
}
```

**Example with cURL:**
```bash
curl -X POST https://your-api.vercel.app/api/v1/generate-post \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence"}'
```

**Example with Python:**
```python
import requests

response = requests.post(
    "https://your-api.vercel.app/api/v1/generate-post",
    json={"topic": "Artificial Intelligence"}
)

result = response.json()
print(result["linkedin_post"])
```

**Example with JavaScript:**
```javascript
const response = await fetch('https://your-api.vercel.app/api/v1/generate-post', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({topic: 'Artificial Intelligence'})
});

const data = await response.json();
console.log(data.linkedin_post);
```

### Health Check

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "LinkedIn Post Generator API",
  "timestamp": "2025-11-04T10:30:00"
}
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=api --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend

# Build to verify no errors
npm run build
```

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `APP_NAME` | Application name | No | "LinkedIn Post Generator" |
| `APP_VERSION` | Application version | No | "1.0.0" |
| `DEBUG` | Debug mode | No | false |
| `CORS_ORIGINS` | Allowed CORS origins | No | ["*"] |
| `LOG_LEVEL` | Logging level | No | INFO |

### Frontend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API URL | No | http://localhost:8000 |

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions.

### Quick Deploy to Vercel

**Backend:**
```bash
cd backend
vercel --prod
```

**Frontend:**
```bash
cd frontend
vercel --prod
```

Don't forget to set environment variables in Vercel dashboard!

## 📁 Project Structure

```
ai-linkedin-post-generator/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── routes/              # API routes
│   │   ├── models/              # Pydantic models
│   │   ├── services/            # Business logic
│   │   └── utils/               # Config & logging
│   ├── tests/                   # Test suite
│   ├── requirements.txt
│   └── vercel.json
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Vue components
│   │   ├── services/            # API calls
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vercel.json
│
├── .github/workflows/           # CI/CD
└── README.md
```

## 🔒 Security Best Practices

- ✅ Never commit `.env` files
- ✅ Use environment variables for secrets
- ✅ Validate all inputs with Pydantic
- ✅ Rate limiting on production (recommended)
- ✅ HTTPS only in production
- ✅ Sanitize user inputs

## 🐛 Troubleshooting

### Common Issues

**"Import errors in Python"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**"API connection failed"**
- Check backend is running on correct port
- Verify `VITE_API_URL` in frontend `.env`
- Check CORS settings

**"Gemini API errors"**
- Verify API key is correct
- Check API quota and billing
- Ensure API is enabled in Google Cloud Console

**"DuckDuckGo search timeout"**
- This is expected occasionally due to rate limiting
- Agent will retry automatically
- Consider implementing fallback search tools

## 🎯 Roadmap

- [ ] Add user authentication (JWT)
- [ ] Implement rate limiting
- [ ] Add Redis caching for frequent topics
- [ ] Support multiple AI models (OpenAI, Claude)
- [ ] Add post scheduling feature
- [ ] Analytics dashboard
- [ ] Browser extension
- [ ] Mobile app (React Native)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini for powerful AI capabilities
- LangChain for AI orchestration
- FastAPI for excellent Python web framework
- Vue.js for reactive UI framework
- Vercel for seamless deployment

## 📞 Contact

**Developer**: Your Name  
**Email**: your.email@example.com  
**LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)  
**Project Link**: [https://github.com/yourusername/linkedin-post-generator](https://github.com/yourusername/linkedin-post-generator)

---

Made with ❤️ and ☕ by [Your Name]
