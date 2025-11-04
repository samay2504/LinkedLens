# 🚀 Deployment Guide

This guide covers deploying the LinkedIn Post Generator to various platforms.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Vercel Deployment](#vercel-deployment)
- [Environment Variables](#environment-variables)
- [CI/CD Setup](#cicd-setup)
- [Monitoring & Logging](#monitoring--logging)
- [Scaling Considerations](#scaling-considerations)

## Prerequisites

### Required Accounts

1. **Google Cloud Account** - For Gemini API
   - Create account at [console.cloud.google.com](https://console.cloud.google.com)
   - Enable Gemini API
   - Generate API key at [makersuite.google.com](https://makersuite.google.com/app/apikey)

2. **Vercel Account** - For hosting
   - Sign up at [vercel.com](https://vercel.com)
   - Install Vercel CLI: `npm install -g vercel`

3. **GitHub Account** - For CI/CD
   - Repository for your code
   - GitHub Actions enabled

## 🔷 Vercel Deployment

### Backend Deployment

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

4. **Set environment variables in Vercel dashboard:**
   - Go to your project settings
   - Navigate to "Environment Variables"
   - Add the following:

   ```
   GEMINI_API_KEY=your_actual_gemini_api_key
   APP_NAME=LinkedIn Post Generator
   APP_VERSION=1.0.0
   DEBUG=false
   LOG_LEVEL=INFO
   CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
   ```

5. **Redeploy to apply environment variables:**
   ```bash
   vercel --prod
   ```

### Frontend Deployment

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Update `.env` with production backend URL:**
   ```
   VITE_API_URL=https://your-backend-url.vercel.app
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

### Vercel Configuration Files

**Backend `vercel.json`:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/main.py"
    }
  ]
}
```

**Frontend `vercel.json`:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}
```

## 🔐 Environment Variables

### Backend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSy...` |
| `APP_NAME` | Application name | `LinkedIn Post Generator` |
| `APP_VERSION` | Version number | `1.0.0` |
| `DEBUG` | Debug mode (false in prod) | `false` |
| `CORS_ORIGINS` | Allowed origins (JSON array) | `["https://frontend.app"]` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Frontend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://api.vercel.app` |

## 🔄 CI/CD Setup

### GitHub Actions Configuration

1. **Add GitHub Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `VERCEL_TOKEN` - Get from [vercel.com/account/tokens](https://vercel.com/account/tokens)
     - `VERCEL_ORG_ID` - Found in Vercel project settings
     - `VERCEL_PROJECT_ID` - Found in Vercel project settings (backend)
     - `VERCEL_FRONTEND_PROJECT_ID` - Found in Vercel project settings (frontend)

2. **Workflows are automatically triggered on:**
   - Push to `main` or `develop` branches
   - Pull requests to `main` branch

3. **Workflow Steps:**
   - Backend CI:
     - Install Python dependencies
     - Run linting with flake8
     - Run pytest with coverage
     - Deploy to Vercel (if main branch)
   
   - Frontend CI:
     - Install Node.js dependencies
     - Build application
     - Deploy to Vercel (if main branch)

## 📊 Monitoring & Logging

### Application Logs

**View Vercel Logs:**
```bash
vercel logs [deployment-url]
```

**Backend logs include:**
- Request/response logging (structlog)
- Error tracking with stack traces
- Agent execution steps
- API call metrics

**Log Levels:**
- `DEBUG` - Detailed information
- `INFO` - General information
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors

### Health Monitoring

**Health Check Endpoint:**
```bash
curl https://your-backend-url.vercel.app/api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "LinkedIn Post Generator API",
  "timestamp": "2025-11-04T10:30:00"
}
```

**Set up monitoring with:**
- [UptimeRobot](https://uptimerobot.com) - Free uptime monitoring
- [Sentry](https://sentry.io) - Error tracking
- [LogRocket](https://logrocket.com) - Session replay

## 📈 Scaling Considerations

### Current Architecture (MVP)

```
User → Vercel Frontend → Vercel Backend (Serverless) → Gemini API
                                                      ↓
                                               DuckDuckGo Search
```

**Limitations:**
- No caching (repeated queries hit API)
- No rate limiting
- No persistent storage
- Cold start delays on serverless

### Scaled Architecture

```
                    ┌─────────────┐
                    │   Vercel    │
                    │  Frontend   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  API Gateway │
                    │ (Rate Limit) │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
  ┌─────▼─────┐     ┌──────▼──────┐    ┌─────▼─────┐
  │   Redis   │     │   FastAPI   │    │ PostgreSQL│
  │  (Cache)  │     │   Backend   │    │ (Storage) │
  └───────────┘     └──────┬──────┘    └───────────┘
                           │
                    ┌──────▼──────┐
                    │   Celery    │
                    │   Workers   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Gemini API │
                    │  + LangChain│
                    └─────────────┘
```

### Recommended Improvements

#### 1. Database Layer (PostgreSQL)

**Purpose:** Store user data, posts, analytics

**Schema:**
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    topic VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    news_sources JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- API usage tracking
CREATE TABLE api_usage (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    endpoint VARCHAR(100),
    status_code INTEGER,
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Implementation:**
```python
# Install: pip install sqlalchemy psycopg2-binary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:pass@host:5432/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

#### 2. Redis Caching

**Purpose:** Cache frequently requested topics, rate limiting

**Implementation:**
```python
# Install: pip install redis
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_result(ttl=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from arguments
            cache_key = f"{func.__name__}:{str(kwargs)}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

# Usage
@cache_result(ttl=3600)  # Cache for 1 hour
async def generate_post(topic: str):
    # ... generation logic
    pass
```

#### 3. Rate Limiting

**Implementation with Redis:**
```python
from fastapi import HTTPException
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, redis_client, max_requests=10, window=60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window
    
    def check_rate_limit(self, user_id: str) -> bool:
        key = f"rate_limit:{user_id}"
        current = self.redis.get(key)
        
        if current is None:
            self.redis.setex(key, self.window, 1)
            return True
        
        if int(current) >= self.max_requests:
            return False
        
        self.redis.incr(key)
        return True

# Usage in route
@router.post("/generate-post")
async def generate_post(
    request: Request,
    limiter: RateLimiter = Depends(get_rate_limiter)
):
    user_id = request.client.host
    if not limiter.check_rate_limit(user_id):
        raise HTTPException(429, "Rate limit exceeded")
    # ... proceed with generation
```

#### 4. Async Task Queue (Celery)

**Purpose:** Handle long-running generation tasks asynchronously

**Installation:**
```bash
pip install celery redis
```

**Configuration:**
```python
# celery_app.py
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def generate_post_async(topic: str):
    agent = NewsToLinkedInAgent(api_key=settings.gemini_api_key)
    result = agent.generate_post(topic)
    return result

# In route
@router.post("/generate-post-async")
async def generate_post_async(request: PostGenerationRequest):
    task = generate_post_async.delay(request.topic)
    return {"task_id": task.id, "status": "processing"}

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }
```

#### 5. CDN & Static Assets

**Use Cloudflare or Vercel CDN:**
- Cache static assets
- Reduce latency globally
- DDoS protection

**Vercel automatically provides:**
- Edge network
- Automatic HTTPS
- Asset optimization

#### 6. Authentication (JWT)

**Implementation:**
```python
# Install: pip install python-jose[cryptography] passlib[bcrypt]
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### Cost Estimation (Scaled)

**For 10,000 users/month:**

| Service | Cost | Notes |
|---------|------|-------|
| Vercel Pro | $20/month | Increased limits |
| PostgreSQL (Supabase) | $25/month | 8GB database |
| Redis (Upstash) | $10/month | 1GB cache |
| Gemini API | ~$50/month | Pay per use |
| Sentry | $26/month | Error tracking |
| **Total** | **~$131/month** | With monitoring |

## 🔧 Deployment Checklist

- [ ] Backend deployed to Vercel
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured in Vercel
- [ ] CORS origins updated for production
- [ ] GitHub Actions workflows configured
- [ ] GitHub secrets added
- [ ] Health check endpoint tested
- [ ] API documentation accessible
- [ ] Monitoring setup (UptimeRobot, Sentry)
- [ ] Domain configured (optional)
- [ ] SSL certificate verified
- [ ] Rate limiting enabled (if scaled)
- [ ] Database backups configured (if scaled)

## 🐛 Troubleshooting Deployment

### Common Issues

**Build Failure:**
- Check build logs in Vercel dashboard
- Verify all dependencies in `requirements.txt` or `package.json`
- Ensure environment variables are set

**API Connection Errors:**
- Verify CORS_ORIGINS includes frontend URL
- Check API_URL in frontend environment
- Test health check endpoint

**Cold Start Delays:**
- Expected with serverless functions
- Consider keeping functions warm with scheduled pings
- Upgrade to Vercel Pro for better performance

## 📞 Support

For deployment issues:
- Check [Vercel Documentation](https://vercel.com/docs)
- GitHub Issues: [Project Issues](https://github.com/yourusername/linkedin-post-generator/issues)
- Email: your.email@example.com

---

Last Updated: November 4, 2025
