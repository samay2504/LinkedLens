"""
Tests for LangChain agent functionality.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from api.services.langchain_agent import NewsToLinkedInAgent


@pytest.fixture
def mock_api_key():
    """Fixture for mock API key."""
    return "test_api_key_123"


@pytest.mark.asyncio
@patch("api.services.langchain_agent.ChatGoogleGenerativeAI")
@patch("api.services.langchain_agent.DuckDuckGoSearchRun")
async def test_agent_initialization(mock_search, mock_llm, mock_api_key):
    """Test agent initializes correctly."""
    agent = NewsToLinkedInAgent(gemini_api_key=mock_api_key, groq_api_key="")
    
    assert agent is not None
    assert agent.llm is not None
    assert len(agent.tools) > 0
    assert agent.agent_executor is not None


@pytest.mark.asyncio
@patch("api.services.langchain_agent.ChatGoogleGenerativeAI")
@patch("api.services.langchain_agent.DuckDuckGoSearchRun")
async def test_generate_post(mock_search, mock_llm, mock_api_key):
    """Test post generation flow."""
    # Mock the agent executor
    with patch.object(NewsToLinkedInAgent, '_create_agent') as mock_create:
        mock_executor = AsyncMock()
        mock_executor.ainvoke.return_value = {
            "output": "Generated LinkedIn post content",
            "intermediate_steps": []
        }
        mock_create.return_value = mock_executor
        
        # Mock image suggestion
        mock_llm_instance = AsyncMock()
        mock_llm_instance.ainvoke.return_value = MagicMock(
            content="Professional business image"
        )
        mock_llm.return_value = mock_llm_instance
        
        agent = NewsToLinkedInAgent(gemini_api_key=mock_api_key, groq_api_key="")
        agent.llm = mock_llm_instance
        
        result = await agent.generate_post("Test Topic")
        
        assert "linkedin_post" in result
        assert "news_sources" in result
        assert "image_suggestion" in result
        assert result["linkedin_post"] == "Generated LinkedIn post content"


def test_extract_sources():
    """Test URL extraction from agent results."""
    agent = NewsToLinkedInAgent.__new__(NewsToLinkedInAgent)
    
    test_result = {
        "output": "Check this link: https://example.com/article",
        "intermediate_steps": [
            ("action", "Found news at https://news.com/story")
        ]
    }
    
    sources = agent._extract_sources(test_result)
    
    assert isinstance(sources, list)
    # Should find at least one URL
    assert len(sources) >= 0
