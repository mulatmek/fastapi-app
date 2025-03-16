import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_post():
    return {
        "title": "test title",
        "content": "test content",
        "published": True,
        "rating": 4,
    }
