"""
Gemini service for direct AI interactions.
Alternative to LangChain for simpler use cases.
"""
import google.generativeai as genai
from typing import Optional
import structlog

logger = structlog.get_logger()


class GeminiService:
    """Direct Gemini API service without LangChain."""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini service.
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_content(self, prompt: str) -> Optional[str]:
        """
        Generate content using Gemini.
        
        Args:
            prompt: Input prompt for generation
        
        Returns:
            Generated content or None if failed
        """
        try:
            logger.info("gemini_generation_started", prompt_length=len(prompt))
            
            response = self.model.generate_content(prompt)
            
            logger.info("gemini_generation_completed")
            return response.text
            
        except Exception as e:
            logger.error("gemini_generation_failed", error=str(e), exc_info=True)
            return None
