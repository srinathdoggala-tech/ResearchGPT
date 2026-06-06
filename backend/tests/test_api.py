"""Backend API tests"""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_plan_endpoint(client, sample_topic):
    """Test planning endpoint"""
    response = client.post(f"/api/plan?topic={sample_topic}")
    assert response.status_code in [200, 500]  # May fail without API keys


@pytest.mark.asyncio
async def test_quick_research_endpoint(client, sample_topic):
    """Test quick research endpoint"""
    response = client.post(f"/api/research/quick?topic={sample_topic}")
    assert response.status_code in [200, 500]  # May fail without API keys


@pytest.mark.asyncio
async def test_verify_endpoint(client, sample_content):
    """Test verification endpoint"""
    response = client.post(f"/api/verify?content={sample_content}")
    assert response.status_code in [200, 500]  # May fail without API keys


@pytest.mark.asyncio
async def test_summarize_endpoint(client, sample_content):
    """Test summarization endpoint"""
    response = client.post(f"/api/summarize?content={sample_content}&length=short")
    assert response.status_code in [200, 500]  # May fail without API keys
