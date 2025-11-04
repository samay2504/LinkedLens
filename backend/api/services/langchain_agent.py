"""
LangChain agent for fetching news and generating LinkedIn posts.
Uses Google Gemini API with Groq as fallback, integrated with multiple search engines.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Optional
import structlog
import re
import os
import requests
from bs4 import BeautifulSoup

logger = structlog.get_logger()

# Check if Groq is available
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logger.warning("langchain_groq not available - Groq fallback disabled")

# Check if Google Search is available
try:
    from googlesearch import search as google_search
    GOOGLE_SEARCH_AVAILABLE = True
except ImportError:
    GOOGLE_SEARCH_AVAILABLE = False
    logger.warning("googlesearch-python not available - Google search fallback disabled")


class NewsToLinkedInAgent:
    """
    LangChain agent that:
    1. Searches for recent news on a topic
    2. Analyzes the content
    3. Generates a LinkedIn-style post
    
    Supports Google Gemini with Groq as fallback.
    """
    
    def __init__(self, gemini_api_key: str, groq_api_key: str = ""):
        """
        Initialize the agent with Gemini API and optional Groq fallback.
        
        Args:
            gemini_api_key: Google Gemini API key
            groq_api_key: Groq API key (fallback)
        """
        self.gemini_api_key = gemini_api_key
        self.groq_api_key = groq_api_key
        self.llm = None
        self.provider = None
        
        # Try Gemini first, then Groq
        try:
            self.llm = self._try_gemini()
            self.provider = "gemini"
            logger.info("llm_initialized", provider="gemini")
        except Exception as e:
            logger.warning("gemini_failed", error=str(e))
            if self.groq_api_key and GROQ_AVAILABLE:
                try:
                    self.llm = self._try_groq()
                    self.provider = "groq"
                    logger.info("llm_initialized", provider="groq")
                except Exception as groq_error:
                    logger.error("groq_failed", error=str(groq_error))
                    raise RuntimeError("Both Gemini and Groq initialization failed") from groq_error
            else:
                raise RuntimeError(f"Gemini failed and no Groq fallback available: {e}") from e
        
        # Initialize web search tool with error handling
        self.tools = [
            Tool(
                name="WebSearch",
                func=self._safe_search,
                description="Search for recent news and articles. Input should be a search query string."
            )
        ]
        
        self.agent_executor = self._create_agent()
    
    def _safe_search(self, query: str) -> str:
        """
        Multi-engine search with fallbacks: Google -> Yahoo -> DuckDuckGo.
        
        Args:
            query: Search query string
            
        Returns:
            Search results from first successful engine
        """
        # Try Google Search first
        if GOOGLE_SEARCH_AVAILABLE:
            try:
                logger.info("attempting_google_search", query=query)
                results = []
                for url in google_search(query, num_results=5, advanced=True):
                    try:
                        # Fetch snippet from the URL
                        response = requests.get(url.url, timeout=5, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        })
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # Get meta description or first paragraph
                        description = soup.find('meta', {'name': 'description'})
                        if description and description.get('content'):
                            snippet = description.get('content')
                        else:
                            paragraph = soup.find('p')
                            snippet = paragraph.get_text()[:200] if paragraph else ""
                        
                        results.append(f"Title: {url.title}\nURL: {url.url}\nSnippet: {snippet}\n")
                    except:
                        results.append(f"Title: {url.title}\nURL: {url.url}\n")
                
                if results:
                    result_text = "\n".join(results)
                    logger.info("google_search_success", query=query, results_count=len(results))
                    return result_text
            except Exception as e:
                logger.warning("google_search_failed", error=str(e), query=query)
        
        # Try Yahoo Search as fallback
        try:
            logger.info("attempting_yahoo_search", query=query)
            yahoo_url = f"https://search.yahoo.com/search?p={requests.utils.quote(query)}"
            response = requests.get(yahoo_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for item in soup.select('.algo, .Sr, div[class*="result"]')[:5]:
                try:
                    title_elem = item.select_one('h3, a')
                    link_elem = item.select_one('a')
                    snippet_elem = item.select_one('.compText, p, span')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text().strip()
                        link = link_elem.get('href', '')
                        snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                        results.append(f"Title: {title}\nURL: {link}\nSnippet: {snippet}\n")
                except:
                    continue
            
            if results:
                result_text = "\n".join(results)
                logger.info("yahoo_search_success", query=query, results_count=len(results))
                return result_text
        except Exception as e:
            logger.warning("yahoo_search_failed", error=str(e), query=query)
        
        # Try DuckDuckGo as final fallback
        try:
            logger.info("attempting_duckduckgo_search", query=query)
            search = DuckDuckGoSearchRun()
            result = search.run(query)
            if result and len(result.strip()) > 0:
                logger.info("duckduckgo_search_success", query=query)
                return result
        except Exception as e:
            logger.warning("duckduckgo_search_failed", error=str(e), query=query)
        
        # All searches failed
        logger.error("all_search_engines_failed", query=query)
        return f"Unable to fetch live search results for '{query}'. Generating content based on general knowledge and recent trends in this topic."
    
    def _try_gemini(self):
        """Try to initialize Gemini LLM with fallback models."""
        logger.info("attempting_gemini_init")
        
        # Try different Gemini models in order of availability
        models_to_try = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro",
        ]
        
        for model in models_to_try:
            try:
                logger.info("trying_gemini_model", model=model)
                llm = ChatGoogleGenerativeAI(
                    model=model,
                    google_api_key=self.gemini_api_key,
                    temperature=0.7,
                    convert_system_message_to_human=True
                )
                # Test with a simple call
                llm.invoke("test")
                logger.info("gemini_model_success", model=model)
                return llm
            except Exception as e:
                logger.warning("gemini_model_failed", model=model, error=str(e))
                continue
        
        raise RuntimeError("All Gemini models failed to initialize")
    
    def _try_groq(self):
        """Try to initialize Groq LLM."""
        if not GROQ_AVAILABLE:
            raise ImportError("langchain_groq not available")
        
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not set")
        
        logger.info("attempting_groq_init")
        
        # Try different Groq models in order of preference
        models_to_try = [
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
        ]
        
        for model in models_to_try:
            try:
                logger.info("trying_groq_model", model=model)
                llm = ChatGroq(
                    groq_api_key=self.groq_api_key,
                    model_name=model,
                    temperature=0.7
                )
                # Test the model with a simple call
                llm.invoke("test")
                logger.info("groq_model_success", model=model)
                return llm
            except Exception as e:
                logger.warning("groq_model_failed", model=model, error=str(e))
                continue
        
        raise RuntimeError("All Groq models failed to initialize")
    
    def _create_agent(self) -> AgentExecutor:
        """
        Create the ReAct agent with custom prompt.
        
        Returns:
            AgentExecutor: Configured agent executor
        """
        template = """You are a professional LinkedIn content creator and news analyst specialising in British English writing.

Your task is to:
1. Search for the most recent and relevant news about: {input}
2. Find 2-3 credible sources
3. Create an engaging LinkedIn post following these strict guidelines:

FORMATTING RULES:
- NO asterisks (*), NO markdown symbols, NO bullet points with symbols
- Use simple numbered points (1., 2., 3.) or write in flowing paragraphs
- NO hyphens, dashes (-, --, ---) or em dashes (—)
- Use commas or full stops instead of dashes
- NO semicolons in casual writing
- NO ellipses (...) unless showing hesitation
- Use colons sparingly, avoid "Key points:" style introductions

LANGUAGE & STYLE (British English):
- Be direct and assertive, eliminate hedging words like "however", "it's worth noting"
- Avoid stock transitions like "furthermore", "in conclusion"
- Use contractions naturally (don't, can't, it's)
- Choose simple words over formal ones (use not utilise, find out not ascertain)
- Vary sentence length for rhythm
- Write conversationally but professionally

CONTENT STRUCTURE:
- Start with a compelling hook or question
- Present 2-3 key insights naturally in flowing text or simple numbered points
- Add thoughtful commentary
- End with an engaging question or call to action
- Include relevant emojis where suitable
- Keep under 300 words
- Write as if speaking to a colleague, not presenting a formal report

You have access to these tools:
{tools}

Tool Names: {tool_names}

Use this format:
Question: the input question
Thought: think about what to do
Action: the action to take (must be one of [{tool_names}])
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Observation as needed)
Thought: I now have enough information to create the post
Final Answer: [Your complete LinkedIn post with NO asterisks, NO markdown symbols, NO dashes]

Begin!

Question: {input}
{agent_scratchpad}
"""
        
        prompt = PromptTemplate.from_template(template)
        agent = create_react_agent(self.llm, self.tools, prompt)
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    async def generate_post(self, topic: str) -> Dict[str, any]:
        """
        Generate LinkedIn post with news sources.
        
        Args:
            topic: Topic to search news about
        
        Returns:
            Dictionary containing:
            - linkedin_post: Generated post content
            - news_sources: List of source URLs
            - image_suggestion: Suggested image description
        
        Raises:
            Exception: If generation fails
        """
        try:
            logger.info("generating_post", topic=topic)
            
            # Run agent
            result = await self.agent_executor.ainvoke({"input": topic})
            
            # Extract sources from agent intermediate steps
            news_sources = self._extract_sources(result)
            
            # Generate image suggestion
            image_suggestion = await self._suggest_image(topic)
            
            logger.info(
                "post_generated",
                topic=topic,
                sources_count=len(news_sources)
            )
            
            return {
                "linkedin_post": result["output"],
                "news_sources": news_sources,
                "image_suggestion": image_suggestion
            }
            
        except Exception as e:
            logger.error("agent_error", error=str(e), topic=topic, exc_info=True)
            raise
    
    def _extract_sources(self, result: Dict) -> List[str]:
        """
        Extract URLs from agent's intermediate steps.
        
        Args:
            result: Agent execution result
        
        Returns:
            List of source URLs (max 3)
        """
        sources = []
        
        try:
            # Check if intermediate_steps exists
            if "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    # Extract URLs from observations
                    if len(step) > 1:
                        observation = str(step[1])
                        # Find URLs in the observation
                        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', observation)
                        sources.extend(urls)
            
            # Also check the output for URLs
            if "output" in result:
                urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', result["output"])
                sources.extend(urls)
            
            # Remove duplicates and limit to 3
            sources = list(dict.fromkeys(sources))[:3]
            
        except Exception as e:
            logger.warning("source_extraction_failed", error=str(e))
        
        return sources if sources else ["Sources from web search"]
    
    async def _suggest_image(self, topic: str) -> Optional[str]:
        """
        Use Gemini to suggest relevant image description.
        
        Args:
            topic: Topic for image suggestion
        
        Returns:
            Image description or None if failed
        """
        try:
            prompt = (
                f"Suggest a professional stock photo description for a LinkedIn post about: {topic}. "
                "Keep it concise (one sentence) and describe what should be in the image. "
                "Focus on professional, business-appropriate imagery."
            )
            
            response = await self.llm.ainvoke(prompt)
            return response.content
            
        except Exception as e:
            logger.warning("image_suggestion_failed", error=str(e))
            return None
