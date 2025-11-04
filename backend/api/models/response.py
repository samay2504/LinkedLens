"""
Pydantic response models for API responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PostGenerationResponse(BaseModel):
    """
    Response model for LinkedIn post generation.
    
    Matches the specification:
    {
      "topic": "Artificial Intelligence",
      "news_sources": ["url1", "url2", "url3"],
      "linkedin_post": "AI is transforming industries... [generated text]",
      "image_suggestion": "Optional image URL or null",
      "generated_at": "2025-11-05T10:30:00"
    }
    """
    
    topic: str = Field(
        description="Original topic requested"
    )
    news_sources: List[str] = Field(
        default_factory=list,
        description="List of news source URLs used for generation"
    )
    linkedin_post: str = Field(
        description="Generated LinkedIn post content in British English style"
    )
    image_suggestion: Optional[str] = Field(
        None,
        description="Suggested image description for the post (null if unavailable)"
    )
    generated_at: datetime = Field(
        description="Timestamp of generation in ISO 8601 format"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Artificial Intelligence",
                "news_sources": [
                    "https://example.com/ai-article-1",
                    "https://example.com/ai-article-2",
                    "https://example.com/ai-article-3"
                ],
                "linkedin_post": "Is AI really changing everything? 🤖\n\nRecent developments show AI is transforming industries at an unprecedented pace.\n\n1. Healthcare diagnostics are now 40% more accurate with AI assistance\n2. Financial institutions are preventing fraud with 95% accuracy\n3. Manufacturing efficiency has improved by 30% through predictive maintenance\n\nWhilst the technology is impressive, the real question is how we ensure ethical implementation. We need frameworks that balance innovation with responsibility.\n\nWhat's your experience with AI in your industry? #ArtificialIntelligence #Technology #Innovation",
                "image_suggestion": "Professional image showing AI neural network visualization with modern technology theme",
                "generated_at": "2025-11-05T10:30:00"
            }
        }
