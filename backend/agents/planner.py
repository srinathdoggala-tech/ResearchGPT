"""Planner Agent - Breaks down research tasks into actionable steps"""

import json
import logging
from typing import Dict, Any
from services.llm import llm_service

logger = logging.getLogger(__name__)


class PlannerAgent:
    """Agent responsible for planning research approach"""
    
    SYSTEM_PROMPT = """You are an expert research planner. When given a research topic, you:
1. Identify the key aspects to research
2. Break down the topic into specific, actionable research questions
3. Suggest the order of investigation
4. Identify potential challenges and how to overcome them

Respond with a JSON object containing:
{
    "topic": "the main research topic",
    "research_questions": ["question1", "question2", ...],
    "research_plan": [
        {
            "step": 1,
            "task": "description",
            "key_focus": "what to look for"
        },
        ...
    ],
    "estimated_duration": "estimated time needed"
}"""
    
    async def plan(self, topic: str) -> Dict[str, Any]:
        """
        Create a research plan for the given topic
        
        Args:
            topic: Research topic
        
        Returns:
            Research plan with questions and steps
        """
        logger.info(f"Planning research for topic: {topic}")
        
        prompt = f"""Create a detailed research plan for the following topic:

Topic: {topic}

Provide a structured approach with specific research questions and steps."""
        
        try:
            response = await llm_service.generate_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                model="openai"
            )
            
            # Parse JSON response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                plan_data = json.loads(response[json_start:json_end])
            else:
                plan_data = self._default_plan(topic)
            
            logger.info(f"Created plan with {len(plan_data.get('research_questions', []))} questions")
            return plan_data
        
        except json.JSONDecodeError:
            logger.warning("Failed to parse plan JSON, using default")
            return self._default_plan(topic)
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return self._default_plan(topic)
    
    def _default_plan(self, topic: str) -> Dict[str, Any]:
        """Provide default plan if generation fails"""
        return {
            "topic": topic,
            "research_questions": [
                f"What is the definition and scope of {topic}?",
                f"What are the current trends in {topic}?",
                f"What are the key challenges in {topic}?"
            ],
            "research_plan": [
                {"step": 1, "task": "Search for general information", "key_focus": "Overview and definitions"},
                {"step": 2, "task": "Research current developments", "key_focus": "Recent trends and updates"},
                {"step": 3, "task": "Identify challenges and opportunities", "key_focus": "Obstacles and solutions"}
            ],
            "estimated_duration": "30-45 minutes"
        }


# Singleton instance
planner_agent = PlannerAgent()
