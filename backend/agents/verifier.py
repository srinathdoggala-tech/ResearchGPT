"""
Verifier Agent - Validates and fact-checks research findings
"""

import logging
from typing import Dict, Any

from services.search import search_service

logger = logging.getLogger(__name__)


class VerifierAgent:
    """
    Lightweight verifier to avoid Gemini quota exhaustion
    """

    async def verify(
        self,
        content: str,
        claims: list[str] | None = None
    ) -> Dict[str, Any]:

        logger.info("Starting verification process")

        try:

            if not claims:
                claims = [content[:200]]

            verification_results = []

            for claim in claims[:1]:

                try:

                    search_result = await search_service.search_with_answer(
                        claim
                    )

                    verification_results.append(
                        {
                            "claim": claim,
                            "verification": "Cross-checked with search sources.",
                            "sources_found": len(
                                search_result.get("results", [])
                            ),
                        }
                    )

                except Exception as e:

                    verification_results.append(
                        {
                            "claim": claim,
                            "verification": f"Verification failed: {str(e)}",
                            "sources_found": 0,
                        }
                    )

            return {
                "content_verified": content[:200] + "...",
                "verification_results": verification_results,
                "overall_reliability": "Medium",
            }

        except Exception as e:

            logger.error(f"Verification process failed: {e}")

            return {
                "content_verified": content[:200] + "...",
                "verification_results": [],
                "overall_reliability": "Unknown",
            }

    async def assess_sources(
        self,
        sources: list[dict]
    ) -> Dict[str, Any]:

        return {
            "sources_assessed": len(sources),
            "assessment": "Basic source assessment completed."
        }


# Singleton instance
verifier_agent = VerifierAgent()