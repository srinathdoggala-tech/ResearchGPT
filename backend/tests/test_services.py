"""Service tests"""

import pytest
from services.llm import llm_service


@pytest.mark.asyncio
async def test_llm_service_initialized():
    """Test LLM service initialization"""
    # Should not raise even if keys not set
    assert llm_service is not None
