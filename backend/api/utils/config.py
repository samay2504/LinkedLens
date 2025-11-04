"""
Environment configuration management using Pydantic Settings.
Loads configuration from .env file with validation.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Keys
    gemini_api_key: str = "test-api-key"  # Default for testing
    groq_api_key: str = ""  # Fallback LLM provider
    
    # Application Settings
    app_name: str = "LinkedIn Post Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS
    cors_origins: List[str] = ["*"]
    
    # Logging
    log_level: str = "INFO"
    
    # LangChain (optional)
    langchain_tracing_v2: str = "false"
    langchain_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Create cached settings instance.
    Uses lru_cache to avoid reading .env file multiple times.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()
