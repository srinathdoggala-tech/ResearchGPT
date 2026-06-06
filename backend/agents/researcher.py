"""Researcher Agent - Conducts research and gathers information"""

import logging
from typing import Dict, Any
from services.llm import llm_service
from services.search import search_service

logger = logging.getLogger(__name__)


class ResearcherAgent:
    """Agent responsible for conducting research"""
    
    SYSTEM_PROMPT = """You are an expert researcher. Your role is to:
1. Understand research questions deeply
2. Search for relevant information
3. Synthesize findings from multiple sources
4. Identify gaps and suggest additional research areas

When analyzing information, focus on:
- Credibility and reliability of sources
- Currency of information
- Relevance to the research question
- Potential biases"""
    
    async def research(self, query: str, context: str = "") -> Dict[str, Any]:
        """
        Conduct research on a specific query
        
        Args:
            query: Research query
            context: Additional context for research
        
        Returns:
            Research findings with sources
        """
        logger.info(f"Researching query: {query}")
        
        try:
            # Search for information
            search_results = await search_service.search(query)
            
            # Prepare research context
            sources_text = "\n".join([
                f"- {r['title']}: {r['snippet']}"
                for r in search_results[:5]
            ])
            
            prompt = f"""Based on the following search results, provide comprehensive research findings.

Research Query: {query}
{f"Additional Context: {context}" if context else ""}

Search Results:
{sources_text}

Please provide:
1. Key findings from the research
2. Supporting evidence from sources
3. Any conflicting information
4. Gaps that need further research

Respond in a structured format with clear sections."""
            
            response = await llm_service.generate_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="openai"
            )

            logger.info(f"Research completed with {len(search_results)} sources")

            return {
                "query": query,
                "findings": response,
                "sources": search_results,
                "source_count": len(search_results)
            }

        except Exception as e:
            logger.error(f"Research failed: {e}")
            # Return safe fallback so API endpoints can respond gracefully
            return {
                "query": query,
                "findings": "[Research failed] Could not perform research at this time.",
                "sources": [],
                "source_count": 0
            }
    
    async def research_stream(self, query: str, context: str = ""):
        """
        Stream research findings
        
        Args:
            query: Research query
            context: Additional context
        
        Yields:
            Research updates
        """
        logger.info(f"Starting streaming research for: {query}")
        
        try:
            # Search for information
            search_results = await search_service.search(query)
            
            sources_text = "\n".join([
                f"- {r['title']}: {r['snippet']}"
                for r in search_results[:5]
            ])
            
            prompt = f"""Based on the following search results, provide comprehensive research findings.

Research Query: {query}
{f"Additional Context: {context}" if context else ""}

Search Results:
{sources_text}

Please provide detailed findings with clear structure."""
            
            async for chunk in llm_service.stream_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="openai"
            ):
                yield chunk

        except Exception as e:
            logger.error(f"Streaming research failed: {e}")
            yield "[Research stream error] Streaming failed"
            return


# Singleton instance
researcher_agent = ResearcherAgent()
