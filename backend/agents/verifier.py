"""Verifier Agent - Validates and fact-checks research findings"""

import logging
from typing import Dict, Any, List
from services.llm import llm_service
from services.search import search_service

logger = logging.getLogger(__name__)


class VerifierAgent:
    """Agent responsible for verifying and fact-checking information"""
    
    SYSTEM_PROMPT = """You are an expert fact-checker and research validator. Your role is to:
1. Identify claims that need verification
2. Search for contradictory or supporting evidence
3. Assess source credibility
4. Identify potential misinformation
5. Provide confidence ratings for claims

When verifying information:
- Cross-reference multiple sources
- Check for recent updates or corrections
- Assess author expertise and bias
- Note limitations and caveats"""
    
    async def verify(self, content: str, claims: List[str] = None) -> Dict[str, Any]:
        """
        Verify research content and fact-check claims
        
        Args:
            content: Content to verify
            claims: Specific claims to verify (optional)
        
        Returns:
            Verification results with accuracy assessment
        """
        logger.info("Starting verification process")
        
        try:
            # Extract claims if not provided
            if not claims:
                claims_prompt = f"""Extract 3-5 key factual claims from the following content that should be verified:

{content}

List the claims clearly, one per line."""
                claims_response = await llm_service.generate_text(
                    prompt=claims_prompt,
                    system_prompt="Extract key factual claims from the given text.",
                    model="openai"
                )
                claims = [line.strip() for line in claims_response.split('\n') if line.strip()]
            
            # Verify each claim
            verification_results = []
            for claim in claims[:5]:  # Limit to 5 claims
                try:
                    search_result = await search_service.search_with_answer(claim)
                    
                    verify_prompt = f"""Verify the following claim:

Claim: {claim}

Supporting information found:
Answer: {search_result.get('answer', 'No direct answer found')}

Sources:
{chr(10).join([f"- {s['title']}: {s['snippet']}" for s in search_result.get('results', [])[:3]])}

Provide a verification assessment including:
1. Accuracy rating (0-100%)
2. Confidence level
3. Supporting evidence
4. Any contradictions found
5. Recommendations"""
                    
                    result_text = await llm_service.generate_text(
                        prompt=verify_prompt,
                        system_prompt=self.SYSTEM_PROMPT,
                        model="openai"
                    )
                    
                    verification_results.append({
                        "claim": claim,
                        "verification": result_text,
                        "sources_found": len(search_result.get('results', []))
                    })
                
                except Exception as e:
                    logger.warning(f"Failed to verify claim '{claim}': {e}")
                    verification_results.append({
                        "claim": claim,
                        "verification": f"Verification failed: {str(e)}",
                        "sources_found": 0
                    })
            
            logger.info(f"Verified {len(verification_results)} claims")
            
            return {
                "content_verified": content[:200] + "...",
                "verification_results": verification_results,
                "overall_reliability": "Good" if len(verification_results) > 0 else "Unknown"
            }
        
        except Exception as e:
            logger.error(f"Verification process failed: {e}")
            raise
    
    async def assess_sources(self, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Assess credibility of sources
        
        Args:
            sources: List of sources with title, URL, snippet
        
        Returns:
            Source assessment results
        """
        logger.info(f"Assessing credibility of {len(sources)} sources")
        
        try:
            assess_prompt = f"""Assess the credibility of the following sources:

Sources:
{chr(10).join([f"- {s['title']} ({s['url']})" for s in sources])}

For each source provide:
1. Credibility rating (Low/Medium/High)
2. Authority assessment
3. Potential biases
4. Overall reliability for research use"""
            
            assessment = await llm_service.generate_text(
                prompt=assess_prompt,
                system_prompt="You are an expert in assessing source credibility and bias.",
                model="openai"
            )
            
            return {
                "sources_assessed": len(sources),
                "assessment": assessment
            }
        
        except Exception as e:
            logger.error(f"Source assessment failed: {e}")
            raise


# Singleton instance
verifier_agent = VerifierAgent()
