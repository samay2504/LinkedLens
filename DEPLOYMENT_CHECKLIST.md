# Quick Deployment Checklist

## Before You Start
- [ ] Vercel CLI installed: `npm install -g vercel`
- [ ] Logged in to Vercel: `vercel login`
- [ ] Gemini API Key ready
- [ ] Groq API Key ready

---

## Step 1: Deploy Backend (5 minutes)

```powershell
cd d:\Projects2.0\Demanualai\backend
vercel --prod
```

- [ ] Backend deployed
- [ ] Backend URL saved: `_______________________________`

### Configure Environment Variables:

```powershell
# Gemini API Key
vercel env add GEMINI_API_KEY production
# Paste your Gemini API key when prompted

# Groq API Key
vercel env add GROQ_API_KEY production
# Paste your Groq API key when prompted

# Temporary CORS
vercel env add CORS_ORIGINS production
# Paste: ["https://*.vercel.app"]

# Redeploy with environment variables
vercel --prod
```

- [ ] Environment variables configured
- [ ] Backend redeployed

### Test Backend:
```powershell
curl https://your-backend-url.vercel.app/api/v1/health
```
- [ ] Health check returns `{"status":"healthy"}`

---

## Step 2: Deploy Frontend (3 minutes)

Create `frontend/.env.production`:
```bash
VITE_API_URL=https://your-backend-url.vercel.app
```

Deploy:
```powershell
cd d:\Projects2.0\Demanualai\frontend
vercel --prod
```

- [ ] Frontend deployed
- [ ] Frontend URL saved: `_______________________________`

---

## Step 3: Update CORS (2 minutes)

```powershell
cd d:\Projects2.0\Demanualai\backend

# Remove temporary CORS
vercel env rm CORS_ORIGINS production

# Add actual frontend URL
vercel env add CORS_ORIGINS production
# Paste: ["https://your-frontend-url.vercel.app"]

# Redeploy backend
vercel --prod
```

- [ ] CORS updated with frontend URL
- [ ] Backend redeployed

---

## Step 4: Verification (5 minutes)

### Test Complete Flow:

1. **Open Frontend**: `https://your-frontend-url.vercel.app`
   - [ ] Page loads correctly
   - [ ] UI displays properly

2. **Generate Post**:
   - [ ] Enter topic: "Artificial Intelligence"
   - [ ] Click "Generate Post"
   - [ ] Loading spinner appears
   - [ ] Post generates successfully
   - [ ] No asterisks (*) in output
   - [ ] British English formatting
   - [ ] News sources display
   - [ ] Image suggestion appears

3. **Check Logs**:
   - [ ] Open Vercel dashboard
   - [ ] Check backend logs
   - [ ] Look for search engine attempts
   - [ ] Verify no errors

---

## Manual Steps Required

### Required Actions:
1. ✅ Run `vercel login` if not logged in
2. ✅ Deploy backend: `cd backend; vercel --prod`
3. ✅ Add environment variables (Gemini key, Groq key, CORS)
4. ✅ Create `frontend/.env.production` with backend URL
5. ✅ Deploy frontend: `cd frontend; vercel --prod`
6. ✅ Update CORS with frontend URL
7. ✅ Test the application

### Automated by Script:
- Requirements.txt with exact versions ✅
- Multi-engine search fallback ✅
- Multi-LLM fallback ✅
- British English formatting ✅
- Error handling ✅
- Logging ✅

---

## Production URLs

After deployment, save these:

```
Backend:  https://_________________________________.vercel.app
Frontend: https://_________________________________.vercel.app
```

---

## Troubleshooting

**If deployment fails:**
1. Check Vercel CLI is installed: `vercel --version`
2. Check logged in: `vercel whoami`
3. Check backend builds locally: `cd backend; pip install -r requirements.txt`
4. Check frontend builds locally: `cd frontend; npm install; npm run build`

**If CORS errors:**
1. Verify CORS_ORIGINS includes frontend URL
2. Format must be: `["https://your-url.vercel.app"]`
3. Redeploy backend after updating

**If API calls fail:**
1. Check VITE_API_URL in frontend/.env.production
2. Test backend directly with curl
3. Check browser console for errors

---

## Success Indicators

✅ Backend health endpoint returns 200
✅ Frontend loads without errors
✅ Post generation works end-to-end
✅ No asterisks in generated posts
✅ British English formatting applied
✅ Search engines working (Google/Yahoo/DuckDuckGo)
✅ News sources display
✅ Image suggestions appear
✅ No CORS errors in browser

---

**Time Estimate: 15 minutes total**
