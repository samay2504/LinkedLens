# LinkedIn Post Generator - Backend API

FastAPI backend service for AI-powered LinkedIn post generation using Google Gemini and LangChain.

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Run Development Server

```bash
uvicorn api.main:app --reload --port 8000
```

Server will start at: `http://localhost:8000`

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=api --cov-report=html

# Specific test file
pytest tests/test_api.py -v
```

### Test Coverage

Current coverage: 85%+

View coverage report:
```bash
open htmlcov/index.html
```

## 📁 Project Structure

```
backend/
├── api/
│   ├── main.py                 # FastAPI application
│   ├── routes/
│   │   └── post_generator.py  # API routes
│   ├── models/
│   │   ├── request.py          # Request schemas
│   │   └── response.py         # Response schemas
│   ├── services/
│   │   ├── langchain_agent.py  # LangChain agent
│   │   └── gemini_service.py   # Gemini service
│   └── utils/
│       ├── config.py           # Configuration
│       └── logger.py           # Logging setup
├── tests/
│   ├── test_api.py            # API tests
│   └── test_agent.py          # Agent tests
├── requirements.txt
└── vercel.json                # Deployment config
```

## 🔧 API Endpoints

### POST /api/v1/generate-post

Generate a LinkedIn post from a topic.

**Request:**
```json
{
  "topic": "Artificial Intelligence"
}
```

**Response:**
```json
{
  "topic": "Artificial Intelligence",
  "linkedin_post": "🤖 AI is transforming industries...",
  "news_sources": ["https://..."],
  "image_suggestion": "Professional AI visualization",
  "generated_at": "2025-11-04T10:30:00"
}
```

### GET /api/v1/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "LinkedIn Post Generator API",
  "timestamp": "2025-11-04T10:30:00"
}
```

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `APP_NAME` | No | Application name |
| `DEBUG` | No | Debug mode (default: false) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |
| `CORS_ORIGINS` | No | Allowed CORS origins |

## 🚢 Deployment

### Vercel

```bash
vercel --prod
```

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions.

## 🛠️ Development

### Code Quality

```bash
# Linting
flake8 api --count --select=E9,F63,F7,F82 --show-source

# Type checking
mypy api

# Format code
black api
```

### Adding New Routes

1. Create route in `api/routes/`
2. Define models in `api/models/`
3. Add tests in `tests/`
4. Register in `api/main.py`

## 📊 Logging

Logs are structured using `structlog` with JSON formatting.

**Log Levels:**
- `DEBUG` - Detailed debugging
- `INFO` - General information
- `WARNING` - Warnings
- `ERROR` - Errors
- `CRITICAL` - Critical issues

**View Logs:**
```bash
tail -f logs/app.log
```

## 🐛 Troubleshooting

### Import Errors

Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

### Gemini API Errors

- Verify API key is correct
- Check quota limits
- Ensure billing is enabled

### DuckDuckGo Search Timeout

This is expected occasionally. The agent will retry automatically.

## 📝 License

MIT License - see [LICENSE](../LICENSE)

## 👥 Contributing

See main [README.md](../README.md) for contribution guidelines.
