# Production Deployment Guide - LinkedIn Post Generator

## 🚀 Overview

This guide covers deploying the AI-Powered LinkedIn Post Generator to Vercel with production-ready configuration.

**Architecture:**
- **Backend**: FastAPI (Python) on Vercel Serverless Functions
- **Frontend**: Vue.js 3 + Vite on Vercel Edge Network
- **AI Providers**: Google Gemini (primary) + Groq (fallback)
- **Search Engines**: Google → Yahoo → DuckDuckGo (triple redundancy)

---

## 📋 Prerequisites

### 1. Install Vercel CLI
```powershell
npm install -g vercel
```

### 2. API Keys Required
- **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Groq API Key**: Get from [Groq Console](https://console.groq.com/keys)

### 3. Vercel Account
- Create account at [vercel.com](https://vercel.com)
- Install Vercel CLI and login: `vercel login`

---

## 🔧 Pre-Deployment Checklist

### Backend Preparation

1. **Verify all dependencies are pinned** ✅
   - Check `backend/requirements.txt` has exact versions
   - All dependencies tested and working locally

2. **Environment variables ready** ✅
   - GEMINI_API_KEY
   - GROQ_API_KEY
   - CORS_ORIGINS (will be updated after frontend deployment)

3. **Code optimizations** ✅
   - Multi-engine search fallback (Google → Yahoo → DuckDuckGo)
   - Multi-LLM fallback (Gemini → Groq)
   - British English formatting
   - Production error handling

### Frontend Preparation

1. **Build configuration** ✅
   - `vercel.json` configured for Vite
   - API URL will be configured after backend deployment

2. **Dependencies verified** ✅
   - All npm packages in `package.json`

---

## 🌐 Step-by-Step Deployment

### Phase 1: Deploy Backend

#### 1.1 Navigate to backend directory
```powershell
cd d:\Projects2.0\Demanualai\backend
```

#### 1.2 Initialize Vercel project (first time only)
```powershell
vercel
```

**Follow the prompts:**
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- What's your project's name? `linkedin-post-generator-backend`
- In which directory is your code located? `./`
- Want to modify settings? **N**

This creates a **development deployment** and gives you a URL like:
`https://linkedin-post-generator-backend-xxx.vercel.app`

#### 1.3 Configure environment variables
```powershell
# Add Gemini API Key
vercel env add GEMINI_API_KEY production
# When prompted, paste your Gemini API key

# Add Groq API Key
vercel env add GROQ_API_KEY production
# When prompted, paste your Groq API key

# Add CORS origins (temporary, will update after frontend deployment)
vercel env add CORS_ORIGINS production

# When prompted, paste: ["https://localhost:5173","https://*.vercel.app"]

# Add other settings
vercel env add APP_NAME production
# Value: LinkedIn Post Generator

vercel env add APP_VERSION production
# Value: 1.0.0

vercel env add DEBUG production
# Value: false

vercel env add LOG_LEVEL production
# Value: INFO
```

#### 1.4 Deploy to production
```powershell
vercel --prod
```

**Save the production URL** (e.g., `https://linkedin-post-generator-backend.vercel.app`)

#### 1.5 Test the backend
```powershell
# Test health endpoint
curl https://your-backend-url.vercel.app/api/v1/health
```

Expected response:
```json
{"status":"healthy","version":"1.0.0"}
```

---

### Phase 2: Deploy Frontend

#### 2.1 Navigate to frontend directory
```powershell
cd d:\Projects2.0\Demanualai\frontend
```

#### 2.2 Create production environment file
Create `frontend/.env.production`:
```bash
VITE_API_URL=https://your-backend-url.vercel.app
```

Replace `your-backend-url.vercel.app` with your actual backend URL from Phase 1.

#### 2.3 Initialize Vercel project
```powershell
vercel
```

**Follow the prompts:**
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- What's your project's name? `linkedin-post-generator-frontend`
- In which directory is your code located? `./`
- Want to modify settings? **N**

#### 2.4 Configure frontend environment variable
```powershell
vercel env add VITE_API_URL production
# When prompted, paste: https://your-backend-url.vercel.app
```

#### 2.5 Deploy to production
```powershell
vercel --prod
```

**Save the production URL** (e.g., `https://linkedin-post-generator.vercel.app`)

---

### Phase 3: Update CORS Configuration

Now that you have the frontend URL, update the backend CORS settings:

#### 3.1 Navigate back to backend
```powershell
cd d:\Projects2.0\Demanualai\backend
```

#### 3.2 Update CORS_ORIGINS
```powershell
# Remove old value
vercel env rm CORS_ORIGINS production

# Add new value with actual frontend URL
vercel env add CORS_ORIGINS production
# When prompted, paste: ["https://your-frontend-url.vercel.app"]
```

Replace `your-frontend-url.vercel.app` with your actual frontend URL.

#### 3.3 Redeploy backend with updated CORS
```powershell
vercel --prod
```

---

## ✅ Post-Deployment Verification

### 1. Test Backend Endpoints

```powershell
# Health check
curl https://your-backend-url.vercel.app/api/v1/health

# Test post generation
curl -X POST https://your-backend-url.vercel.app/api/v1/generate-post `
  -H "Content-Type: application/json" `
  -d '{"topic":"Artificial Intelligence trends"}'
```

### 2. Test Frontend Application

1. Open `https://your-frontend-url.vercel.app` in browser
2. Enter a topic (e.g., "Artificial Intelligence")
3. Click "Generate Post"
4. Verify:
   - Loading spinner appears
   - Post generates successfully
   - News sources appear
   - Image suggestion displays
   - British English formatting (no asterisks, proper style)

### 3. Test Fallback Systems

**Test Search Engine Fallback:**
- Generate posts on various topics
- Check backend logs in Vercel dashboard
- Should see attempts across Google/Yahoo/DuckDuckGo

**Test LLM Fallback:**
- If Gemini quota exhausted, should automatically use Groq
- Check logs for "attempting_groq_init" messages

---

## 🔍 Monitoring & Logs

### View Backend Logs
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your backend project
3. Click "Logs" or "Functions"
4. Monitor requests, errors, and search engine attempts

### View Frontend Logs
1. Select your frontend project in Vercel dashboard
2. Check "Deployments" for build logs
3. Check "Analytics" for user activity

### Key Metrics to Monitor
- ✅ Search engine success rates (Google/Yahoo/DuckDuckGo)
- ✅ LLM provider usage (Gemini vs Groq)
- ✅ API response times
- ✅ Error rates and types

---

## 🐛 Troubleshooting

### Issue: Backend deployment fails

**Solution:**
```powershell
# Check requirements.txt syntax
cd backend
d:\Projects2.0\Demanualai\.conda\python.exe -m pip install -r requirements.txt

# If successful locally, try deploying again
vercel --prod
```

### Issue: CORS errors in browser

**Solution:**
1. Verify CORS_ORIGINS includes your frontend URL
2. Check format: `["https://your-frontend.vercel.app"]`
3. Redeploy backend after updating

### Issue: API calls failing from frontend

**Solution:**
1. Check `VITE_API_URL` in frontend environment variables
2. Verify URL includes `https://` and no trailing slash
3. Test backend endpoint directly with curl
4. Check browser console for exact error

### Issue: Search engines failing

**Solution:**
- System has triple redundancy (Google → Yahoo → DuckDuckGo)
- Check backend logs to see which engines are being attempted
- If all fail, check if IP is rate-limited
- Vercel functions may need User-Agent headers (already implemented)

### Issue: Gemini API quota exceeded

**Solution:**
- System automatically falls back to Groq
- Check logs for "attempting_groq_init"
- Verify GROQ_API_KEY is set correctly
- Get additional Gemini quota or wait for reset

---

## 🔐 Security Best Practices

### Environment Variables
- ✅ Never commit `.env` files to git
- ✅ Use Vercel's environment variable system
- ✅ Rotate API keys periodically
- ✅ Use different keys for development/production

### API Rate Limiting
- Consider implementing rate limiting on backend
- Monitor API usage in Gemini/Groq dashboards
- Set up alerts for quota thresholds

### CORS Configuration
- Only allow specific frontend domains
- Don't use wildcard (*) in production
- Update CORS_ORIGINS when adding new domains

---

## 📊 Performance Optimization

### Backend
- ✅ Serverless functions auto-scale
- ✅ Multi-engine search reduces failures
- ✅ Multi-LLM fallback ensures availability
- ✅ Structured logging for monitoring

### Frontend
- ✅ Built with Vite (optimized bundles)
- ✅ Deployed on Vercel Edge Network (global CDN)
- ✅ Automatic caching and compression

---

## 🔄 Updating Deployment

### Update Backend
```powershell
cd d:\Projects2.0\Demanualai\backend
# Make your changes
vercel --prod
```

### Update Frontend
```powershell
cd d:\Projects2.0\Demanualai\frontend
# Make your changes
vercel --prod
```

### Update Environment Variables
```powershell
# List all environment variables
vercel env ls

# Update a variable
vercel env rm VARIABLE_NAME production
vercel env add VARIABLE_NAME production

# Redeploy to apply changes
vercel --prod
```

---

## 📱 Custom Domain (Optional)

### Add Custom Domain

1. Go to your project in Vercel dashboard
2. Click "Settings" → "Domains"
3. Add your domain (e.g., `linkedinai.yourdomain.com`)
4. Update DNS records as instructed by Vercel
5. Update CORS_ORIGINS to include custom domain

---

## ✨ Success Criteria

Your deployment is successful when:

- ✅ Backend health endpoint responds with 200
- ✅ Frontend loads and displays UI correctly
- ✅ Post generation works end-to-end
- ✅ Search results appear from Google/Yahoo/DuckDuckGo
- ✅ British English formatting (no asterisks, proper style)
- ✅ LLM fallback works (Gemini → Groq)
- ✅ Image suggestions generate
- ✅ News sources display
- ✅ No CORS errors in browser console
- ✅ Logs show proper error handling

---

## 📞 Support Resources

- **Vercel Documentation**: https://vercel.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Google Gemini API**: https://ai.google.dev/docs
- **Groq API**: https://console.groq.com/docs

---

## 🎯 Production URLs

After deployment, save these URLs:

```
Backend:  https://linkedin-post-generator-backend.vercel.app
Frontend: https://linkedin-post-generator.vercel.app
```

**Deployment completed successfully! 🎉**
