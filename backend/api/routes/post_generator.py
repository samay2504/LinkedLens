"""
FastAPI routes for LinkedIn post generation.
"""
from fastapi import APIRouter, HTTPException, Depends
from api.models.request import PostGenerationRequest
from api.models.response import PostGenerationResponse
from api.services.langchain_agent import NewsToLinkedInAgent
from api.utils.config import get_settings, Settings
from api.utils.logger import setup_logging
import structlog
from datetime import datetime
from typing import Dict

router = APIRouter(prefix="/api/v1", tags=["Post Generation"])
logger = structlog.get_logger()

# Cache agent instance
_agent_instance = None


def get_agent(settings: Settings = Depends(get_settings)) -> NewsToLinkedInAgent:
    """
    Dependency injection for agent with caching.
    
    Args:
        settings: Application settings
    
    Returns:
        NewsToLinkedInAgent: Cached agent instance
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = NewsToLinkedInAgent(
            gemini_api_key=settings.gemini_api_key,
            groq_api_key=settings.groq_api_key
        )
    return _agent_instance


@router.post("/generate-post", response_model=PostGenerationResponse)
async def generate_linkedin_post(
    request: PostGenerationRequest,
    agent: NewsToLinkedInAgent = Depends(get_agent)
) -> PostGenerationResponse:
    """
    Generate a LinkedIn post from recent news on a given topic.
    
    **Endpoint:** POST /api/v1/generate-post
    
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
    
    This endpoint:
    1. Searches for recent news about the specified topic using multi-engine fallback (Google → Yahoo → DuckDuckGo)
    2. Analyzes and synthesizes the information using Google Gemini AI (with Groq fallback)
    3. Creates a professional LinkedIn post in British English style
    4. Suggests relevant imagery
    
    Args:
        request: PostGenerationRequest with topic field
        agent: Injected NewsToLinkedInAgent instance
    
    Returns:
        PostGenerationResponse: Generated post with metadata
    
    Raises:
        HTTPException: If generation fails (500)
    """
    try:
        logger.info(
            "post_generation_request",
            topic=request.topic,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Generate post using agent
        result = await agent.generate_post(request.topic)
        
        # Build response
        response = PostGenerationResponse(
            topic=request.topic,
            news_sources=result["news_sources"],
            linkedin_post=result["linkedin_post"],
            image_suggestion=result.get("image_suggestion"),
            generated_at=datetime.utcnow()
        )
        
        logger.info(
            "post_generated_successfully",
            topic=request.topic,
            post_length=len(response.linkedin_post)
        )
        
        return response
        
    except Exception as e:
        logger.error(
            "post_generation_failed",
            error=str(e),
            topic=request.topic,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate post: {str(e)}"
        )


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        Dict with status and timestamp
    """
    return {
        "status": "healthy",
        "service": "LinkedIn Post Generator API",
        "timestamp": datetime.utcnow().isoformat()
    }
