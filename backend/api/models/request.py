"""
Pydantic request models for API validation.
"""
from pydantic import BaseModel, Field


class PostGenerationRequest(BaseModel):
    """Request model for LinkedIn post generation."""
    
    topic: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Topic to search news about and generate LinkedIn post",
        examples=["Artificial Intelligence in Healthcare", "Climate Change Policy"]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Artificial Intelligence"
            }
        }
