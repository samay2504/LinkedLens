# Quick Deployment Script for LinkedIn Post Generator
# Run this script to deploy both backend and frontend to Vercel

Write-Host "🚀 LinkedIn Post Generator - Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "======================================================`n" -ForegroundColor Cyan

# Check if Vercel CLI is installed
Write-Host "Checking Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version
    Write-Host "✅ Vercel CLI installed: $vercelVersion`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
    Write-Host "✅ Vercel CLI installed`n" -ForegroundColor Green
}

# Check if logged in to Vercel
Write-Host "Checking Vercel authentication..." -ForegroundColor Yellow
$loggedIn = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not logged in to Vercel" -ForegroundColor Red
    Write-Host "Please run: vercel login`n" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Logged in as: $loggedIn`n" -ForegroundColor Green

# Prompt for API keys
Write-Host "📝 Environment Configuration" -ForegroundColor Cyan
Write-Host "============================`n" -ForegroundColor Cyan

$geminiKey = Read-Host "Enter your GEMINI_API_KEY (or press Enter to skip)"
$groqKey = Read-Host "Enter your GROQ_API_KEY (or press Enter to skip)"

# Deploy Backend
Write-Host "`n🔧 Deploying Backend..." -ForegroundColor Cyan
Write-Host "========================`n" -ForegroundColor Cyan

Set-Location "d:\Projects2.0\Demanualai\backend"

Write-Host "Running backend deployment..." -ForegroundColor Yellow
vercel --prod

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Backend deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Backend deployed successfully!" -ForegroundColor Green
$backendUrl = Read-Host "`nEnter your backend URL (e.g., https://your-backend.vercel.app)"

# Configure backend environment variables if keys provided
if ($geminiKey) {
    Write-Host "`nConfiguring GEMINI_API_KEY..." -ForegroundColor Yellow
    $geminiKey | vercel env add GEMINI_API_KEY production
}

if ($groqKey) {
    Write-Host "Configuring GROQ_API_KEY..." -ForegroundColor Yellow
    $groqKey | vercel env add GROQ_API_KEY production
}

# Deploy Frontend
Write-Host "`n🎨 Deploying Frontend..." -ForegroundColor Cyan
Write-Host "========================`n" -ForegroundColor Cyan

Set-Location "d:\Projects2.0\Demanualai\frontend"

# Create .env.production with backend URL
$envContent = "VITE_API_URL=$backendUrl"
Set-Content -Path ".env.production" -Value $envContent
Write-Host "✅ Created .env.production with backend URL`n" -ForegroundColor Green

Write-Host "Running frontend deployment..." -ForegroundColor Yellow
vercel --prod

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Frontend deployed successfully!" -ForegroundColor Green
$frontendUrl = Read-Host "`nEnter your frontend URL (e.g., https://your-frontend.vercel.app)"

# Update CORS configuration
Write-Host "`n🔐 Updating CORS Configuration..." -ForegroundColor Cyan
Write-Host "==================================`n" -ForegroundColor Cyan

Set-Location "d:\Projects2.0\Demanualai\backend"

$corsOrigins = "[`"$frontendUrl`"]"
Write-Host "Setting CORS_ORIGINS to: $corsOrigins" -ForegroundColor Yellow
$corsOrigins | vercel env add CORS_ORIGINS production

Write-Host "`nRedeploying backend with updated CORS..." -ForegroundColor Yellow
vercel --prod

# Summary
Write-Host "`n✨ Deployment Complete!" -ForegroundColor Green
Write-Host "=====================`n" -ForegroundColor Green

Write-Host "Backend URL:  $backendUrl" -ForegroundColor Cyan
Write-Host "Frontend URL: $frontendUrl`n" -ForegroundColor Cyan

Write-Host "🧪 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Test backend health: $backendUrl/api/v1/health" -ForegroundColor White
Write-Host "2. Open frontend: $frontendUrl" -ForegroundColor White
Write-Host "3. Generate a test post" -ForegroundColor White
Write-Host "4. Check logs in Vercel dashboard`n" -ForegroundColor White

Write-Host "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md`n" -ForegroundColor Cyan

# Return to root directory
Set-Location "d:\Projects2.0\Demanualai"
