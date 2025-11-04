"""
FastAPI main application entry point.
Configures middleware, routes, and lifecycle events.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import post_generator
from api.utils.config import get_settings
from api.utils.logger import setup_logging
import structlog

# Initialize settings and logging
settings = get_settings()
logger = setup_logging(settings.log_level)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered LinkedIn post generator using Google Gemini API and LangChain. "
                "Fetches recent news and creates engaging LinkedIn content.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(post_generator.router)


@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup.
    Logs startup information.
    """
    logger.info(
        "application_startup",
        version=settings.app_version,
        app_name=settings.app_name,
        debug=settings.debug
    )


@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown.
    Cleanup and final logging.
    """
    logger.info("application_shutdown")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Dict with API metadata and links
    """
    return {
        "message": "LinkedIn Post Generator API",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health"
    }
