"""Researcher Agent - Conducts research and gathers information"""

import logging
from typing import Dict, Any

from services.llm import llm_service
from services.search import search_service

logger = logging.getLogger(__name__)


class ResearcherAgent:
    """Agent responsible for conducting research"""

    SYSTEM_PROMPT = """
You are an expert researcher.

Your job:

1. Analyze search results
2. Extract useful information
3. Synthesize findings
4. Mention limitations
5. Use evidence from sources

Write clear structured findings.
"""

    async def research(
        self,
        query: str,
        context: str = ""
    ) -> Dict[str, Any]:

        logger.info(f"Researching: {query}")

        try:

            search_results = await search_service.search(query)

            sources_text = "\n".join(
                [
                    f"- {item['title']}: {item['snippet']}"
                    for item in search_results[:5]
                ]
            )

            prompt = f"""
Research Topic:

{query}

Context:
{context}

Sources:
{sources_text}

Provide:

1. Overview
2. Key findings
3. Trends
4. Challenges
5. Conclusion
"""

            findings = await llm_service.generate_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="gemini"
            )

            return {
                "query": query,
                "findings": findings,
                "sources": search_results,
                "source_count": len(search_results)
            }

        except Exception as e:

            logger.error(f"Research failed: {e}")

            return {
                "query": query,
                "findings": f"[Research Failed]\n\n{str(e)}",
                "sources": [],
                "source_count": 0
            }

    async def research_stream(
        self,
        query: str,
        context: str = ""
    ):

        try:

            search_results = await search_service.search(query)

            sources_text = "\n".join(
                [
                    f"- {item['title']}: {item['snippet']}"
                    for item in search_results[:5]
                ]
            )

            prompt = f"""
Research Topic:

{query}

Context:
{context}

Sources:
{sources_text}

Provide detailed research findings.
"""

            async for chunk in llm_service.stream_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="gemini"
            ):
                yield chunk

        except Exception as e:

            logger.error(f"Research stream failed: {e}")

            yield f"[Research Stream Error] {str(e)}"


researcher_agent = ResearcherAgent()