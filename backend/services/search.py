"""Search Service - Web search capabilities"""

import asyncio
import logging
from typing import List, Dict, Any
from config import settings

# Optional import for Tavily search client. Keep module import-safe
try:
    from tavily import TavilyClient
except Exception:
    TavilyClient = None

logger = logging.getLogger(__name__)


class SearchService:
    """Service for web search"""
    
    def __init__(self):
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize search client"""
        if TavilyClient is not None and settings.tavily_api_key:
            try:
                self.client = TavilyClient(api_key=settings.tavily_api_key)
                logger.info("✓ Initialized Tavily search client")
            except Exception as e:
                logger.error(f"Failed to initialize Tavily client: {e}")
        else:
            if not settings.tavily_api_key:
                logger.info("Tavily API key not configured; search disabled")
            else:
                logger.info("Tavily client library not available; search disabled")
    
    async def search(self, query: str, max_results: int = None) -> List[Dict[str, Any]]:
        """
        Search the web for information
        
        Args:
            query: Search query
            max_results: Maximum number of results (defaults to config)
        
        Returns:
            List of search results with title, URL, and snippet
        """
        if not self.client:
            # Return empty results rather than raising, to allow the app to
            # operate in environments without a search API key or client.
            logger.warning("Search client not configured; returning empty results")
            return []
        
        max_results = max_results or settings.search_max_results
        
        try:
            logger.info(f"Searching for: {query}")
            # Run search in thread pool to avoid blocking
            result = await asyncio.to_thread(
                self.client.search,
                query,
                max_results=max_results,
                include_answer=True
            )
            
            # Format results
            formatted_results = []
            for item in result.get("results", []):
                formatted_results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                    "content": item.get("content", "")
                })
            
            logger.info(f"Found {len(formatted_results)} results")
            return formatted_results
        
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise ValueError(f"Search failed: {str(e)}")
    
    async def search_with_answer(self, query: str) -> Dict[str, Any]:
        """
        Search and get direct answer
        
        Args:
            query: Search query
        
        Returns:
            Dictionary with answer and sources
        """
        if not self.client:
            logger.warning("Search client not configured; returning empty answer")
            return {"answer": "", "results": []}
        
        try:
            result = await asyncio.to_thread(
                self.client.search,
                query,
                max_results=settings.search_max_results,
                include_answer=True
            )
            
            return {
                "answer": result.get("answer", ""),
                "results": [
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("snippet", "")
                    }
                    for item in result.get("results", [])
                ]
            }
        
        except Exception as e:
            logger.error(f"Search with answer failed: {e}")
            raise ValueError(f"Search failed: {str(e)}")


# Singleton instance
search_service = SearchService()
