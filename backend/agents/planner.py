"""Planner Agent - Breaks down research tasks into actionable steps"""

import json
import logging
from typing import Dict, Any

from services.llm import llm_service

logger = logging.getLogger(__name__)


class PlannerAgent:
    """Agent responsible for planning research approach"""

    SYSTEM_PROMPT = """
You are an expert research planner.

When given a topic:

1. Identify key research areas
2. Generate research questions
3. Create a step-by-step plan
4. Estimate effort

Return ONLY valid JSON.

Example:

{
  "topic": "Artificial Intelligence",
  "research_questions": [
    "What is AI?",
    "What are current trends?",
    "What are the challenges?"
  ],
  "research_plan": [
    {
      "step": 1,
      "task": "Understand fundamentals",
      "key_focus": "Definitions and concepts"
    }
  ],
  "estimated_duration": "30 minutes"
}
"""

    async def plan(self, topic: str) -> Dict[str, Any]:

        logger.info(f"Planning topic: {topic}")

        prompt = f"""
Create a research plan for:

Topic: {topic}
"""

        try:

            response = await llm_service.generate_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="gemini"
            )

            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])

            return self._default_plan(topic)

        except Exception as e:

            logger.error(f"Planner failed: {e}")

            return self._default_plan(topic)

    def _default_plan(self, topic: str):

        return {
            "topic": topic,
            "research_questions": [
                f"What is {topic}?",
                f"What are the current developments in {topic}?",
                f"What are the major challenges in {topic}?"
            ],
            "research_plan": [
                {
                    "step": 1,
                    "task": "Understand fundamentals",
                    "key_focus": "Definitions"
                },
                {
                    "step": 2,
                    "task": "Research current trends",
                    "key_focus": "Latest developments"
                },
                {
                    "step": 3,
                    "task": "Analyze challenges",
                    "key_focus": "Problems and solutions"
                }
            ],
            "estimated_duration": "30 minutes"
        }


planner_agent = PlannerAgent()