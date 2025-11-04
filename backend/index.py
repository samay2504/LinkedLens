"""
Vercel serverless function handler for FastAPI application.
"""
from mangum import Mangum
from api.main import app

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app, lifespan="off")
