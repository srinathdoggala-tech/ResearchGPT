"""Test configuration"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def sample_topic():
    """Sample research topic"""
    return "Artificial Intelligence"


@pytest.fixture
def sample_content():
    """Sample content for testing"""
    return "AI is transforming technology. Machine learning enables systems to learn from data."
