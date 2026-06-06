"""Writer Agent - Synthesizes research into polished output"""

import logging
from typing import Dict, Any
from services.llm import llm_service

logger = logging.getLogger(__name__)


class WriterAgent:
    """Agent responsible for writing and synthesizing research"""
    
    SYSTEM_PROMPT = """You are an expert technical writer and researcher. Your role is to:
1. Synthesize research findings into coherent narratives
2. Create well-structured reports and articles
3. Ensure clarity and accessibility
4. Properly cite sources
5. Maintain academic integrity
6. Adapt tone and style to audience

When writing:
- Use clear, concise language
- Structure information logically
- Provide proper context and background
- Include relevant examples
- Cite sources appropriately"""
    
    async def write_report(
        self,
        topic: str,
        findings: Dict[str, Any],
        style: str = "academic"
    ) -> Dict[str, Any]:
        """
        Write a research report
        
        Args:
            topic: Research topic
            findings: Research findings from researcher agent
            style: Writing style (academic, journalistic, summary)
        
        Returns:
            Written report
        """
        logger.info(f"Writing {style} report for topic: {topic}")
        
        try:
            findings_text = findings.get('findings', '')
            sources_text = "\n".join([
                f"- {s['title']}: {s['url']}"
                for s in findings.get('sources', [])[:5]
            ])
            
            prompt = f"""Write a comprehensive research report on: {topic}

Research Findings:
{findings_text}

Sources:
{sources_text}

Style: {style}
Format: Clear sections with introduction, main findings, analysis, and conclusion.
Include proper source citations."""
            
            report = await llm_service.generate_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="openai"
            )
            
            word_count = len(report.split())
            logger.info(f"Generated {word_count} word report")
            
            return {
                "topic": topic,
                "style": style,
                "report": report,
                "word_count": word_count
            }
        
        except Exception as e:
            logger.error(f"Report writing failed: {e}")
            raise
    
    async def write_summary(
        self,
        content: str,
        length: str = "medium"
    ) -> Dict[str, str]:
        """
        Create a summary of research content
        
        Args:
            content: Content to summarize
            length: Summary length
        
        Returns:
            Summary result
        """
        logger.info(f"Creating {length} summary")
        
        try:
            length_map = {
                "short": "2-3 paragraphs",
                "medium": "4-6 paragraphs",
                "long": "full summary with multiple sections"
            }
            
            prompt = f"""Create a {length_map.get(length, 'comprehensive')} summary of the following research:

{content}

Focus on key points, main findings, and actionable insights."""
            
            summary = await llm_service.generate_text(
                prompt=prompt,
                system_prompt="You are an expert at creating clear, concise summaries.",
                model="openai"
            )
            
            return {
                "original_length": len(content.split()),
                "summary_length": len(summary.split()),
                "summary": summary
            }
        
        except Exception as e:
            logger.error(f"Summary creation failed: {e}")
            raise
    
    async def write_stream(
        self,
        topic: str,
        findings: Dict[str, Any],
        style: str = "academic"
    ):
        """
        Stream write a research report
        
        Args:
            topic: Research topic
            findings: Research findings
            style: Writing style
        
        Yields:
            Report text chunks
        """
        logger.info(f"Starting streaming write for: {topic}")
        
        try:
            findings_text = findings.get('findings', '')
            sources_text = "\n".join([
                f"- {s['title']}: {s['url']}"
                for s in findings.get('sources', [])[:5]
            ])
            
            prompt = f"""Write a comprehensive research report on: {topic}

Research Findings:
{findings_text}

Sources:
{sources_text}

Style: {style}
Format: Clear sections with introduction, main findings, analysis, and conclusion."""
            
            async for chunk in llm_service.stream_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="openai"
            ):
                yield chunk
        
        except Exception as e:
            logger.error(f"Streaming write failed: {e}")
            raise


# Singleton instance
writer_agent = WriterAgent()
