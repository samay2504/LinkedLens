"""
Tests for FastAPI endpoints.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from api.main import app
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint returns correct information."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_generate_post_validation():
    """Test post generation with invalid input."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Empty topic
        response = await client.post("/api/v1/generate-post", json={"topic": ""})
        assert response.status_code == 422
        
        # Topic too short
        response = await client.post("/api/v1/generate-post", json={"topic": "AI"})
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_post_success():
    """Test successful post generation."""
    # Create a mock agent
    mock_agent = AsyncMock()
    mock_agent.generate_post.return_value = {
        "linkedin_post": "Test LinkedIn post content",
        "news_sources": ["https://example.com/news"],
        "image_suggestion": "Professional AI image"
    }
    
    # Override the dependency
    from api.routes.post_generator import get_agent
    app.dependency_overrides[get_agent] = lambda: mock_agent
    
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/generate-post",
                json={"topic": "Artificial Intelligence"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Artificial Intelligence"
        assert "linkedin_post" in data
        assert "news_sources" in data
        assert "generated_at" in data
    finally:
        # Clean up dependency override
        app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.integration  # Mark as integration test
async def test_gemini_api_key_validation():
    """
    Integration test: Validates that the Gemini API key actually works.
    This makes a real API call to Gemini.
    
    Run with: pytest -m integration
    Skip with: pytest -m "not integration"
    """
    from api.utils.config import get_settings
    import google.generativeai as genai
    import os
    
    # Clear the settings cache to force reload from .env
    get_settings.cache_clear()
    
    # Force reload environment variables
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    settings = get_settings()
    
    # Skip if using test key
    if settings.gemini_api_key == "test-api-key" or not settings.gemini_api_key:
        pytest.skip("Skipping integration test: No real API key configured")
    
    try:
        # Configure Gemini with the API key
        genai.configure(api_key=settings.gemini_api_key)
        
        # List available models first
        try:
            models = genai.list_models()
            available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            print(f"\n📋 Available models: {available_models}")
            if available_models:
                model_name = available_models[0].split('/')[-1]  # Get first available model
            else:
                pytest.skip("No models available for generateContent")
        except:
            # Fallback to try common model names
            model_name = 'models/gemini-pro'
        
        # Try to create a model and generate content
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'API key works!' if you can read this.")
        
        # If we get here without exception, the API key works
        assert response.text is not None
        assert len(response.text) > 0
        print(f"\n✅ API Key validated! Model: {model_name}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        pytest.fail(f"Gemini API key validation failed: {str(e)}")


@pytest.mark.asyncio
@pytest.mark.integration  # Mark as integration test
async def test_generate_post_real_api():
    """
    Integration test: Test full post generation with real Gemini API.
    This makes real API calls.
    
    Run with: pytest -m integration
    Skip with: pytest -m "not integration"
    """
    from api.utils.config import get_settings
    from dotenv import load_dotenv
    
    # Clear cache and reload env
    get_settings.cache_clear()
    load_dotenv(override=True)
    
    settings = get_settings()
    
    # Skip if using test key
    if settings.gemini_api_key == "test-api-key" or not settings.gemini_api_key:
        pytest.skip("Skipping integration test: No real API key configured")
    
    # Clear any dependency overrides
    app.dependency_overrides.clear()
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", timeout=60.0) as client:
        response = await client.post(
            "/api/v1/generate-post",
            json={"topic": "Artificial Intelligence"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Artificial Intelligence"
    assert "linkedin_post" in data
    assert len(data["linkedin_post"]) > 50  # Should be a real post
    assert "news_sources" in data
    assert "generated_at" in data
    print(f"\n✅ Post generated successfully!")
    print(f"Post preview: {data['linkedin_post'][:200]}...")
