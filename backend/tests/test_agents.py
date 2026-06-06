"""Agent tests"""

import pytest
from agents.planner import planner_agent


@pytest.mark.asyncio
async def test_planner_agent(sample_topic):
    """Test planner agent"""
    try:
        plan = await planner_agent.plan(sample_topic)
        assert "topic" in plan
        assert "research_questions" in plan
        assert "research_plan" in plan
    except ValueError:
        # Expected if API keys not set
        pytest.skip("API keys not configured")
