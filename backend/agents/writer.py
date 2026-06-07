"""Writer Agent - Synthesizes research into polished output"""

import logging
from typing import Dict, Any
from services.llm import llm_service

logger = logging.getLogger(__name__)


class WriterAgent:

    SYSTEM_PROMPT = """
You are an expert technical writer.

Create clear, professional research reports.

Use:
- Introduction
- Main Findings
- Analysis
- Conclusion

Keep responses factual and well structured.
"""

    async def write_report(
        self,
        topic: str,
        findings: Dict[str, Any],
        style: str = "academic"
    ) -> Dict[str, Any]:

        logger.info(f"Writing report for: {topic}")

        try:

            findings_text = findings.get("findings", "")

            sources_text = "\n".join([
                f"- {s.get('title','')} : {s.get('url','')}"
                for s in findings.get("sources", [])[:5]
            ])

            prompt = f"""
Topic:
{topic}

Research Findings:
{findings_text}

Sources:
{sources_text}

Writing Style:
{style}

Generate a complete report.
"""

            report = await llm_service.generate_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="gemini"
            )

            return {
                "topic": topic,
                "style": style,
                "report": report,
                "word_count": len(report.split())
            }

        except Exception as e:

            logger.error(f"Report generation failed: {e}")

            return {
                "topic": topic,
                "style": style,
                "report": "[REPORT GENERATION FAILED]",
                "word_count": 0
            }

    async def write_summary(
        self,
        content: str,
        length: str = "medium"
    ) -> Dict[str, str]:

        try:

            prompt = f"""
Summarize the following content.

Length: {length}

Content:
{content}
"""

            summary = await llm_service.generate_text(
                prompt=prompt,
                system_prompt="Create a concise summary.",
                model="gemini"
            )

            return {
                "original_length": len(content.split()),
                "summary_length": len(summary.split()),
                "summary": summary
            }

        except Exception as e:

            logger.error(f"Summary failed: {e}")

            return {
                "original_length": len(content.split()),
                "summary_length": 0,
                "summary": "[SUMMARY FAILED]"
            }

    async def write_stream(
        self,
        topic: str,
        findings: Dict[str, Any],
        style: str = "academic"
    ):

        try:

            findings_text = findings.get("findings", "")

            prompt = f"""
Topic: {topic}

Research Findings:
{findings_text}

Style:
{style}

Generate report.
"""

            async for chunk in llm_service.stream_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="gemini"
            ):
                yield chunk

        except Exception as e:

            logger.error(f"Streaming failed: {e}")

            yield "[STREAM FAILED]"


writer_agent = WriterAgent()