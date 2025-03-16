import pytest
from fastapi import status


def test_create_post_invalid_data(client):
    """Test creating a post with invalid data"""
    invalid_post = {
        "title": "",  # Empty title
        "content": None,  # Invalid content type
        "published": "not a boolean",  # Invalid boolean
        "rating": "not a number",  # Invalid rating type
    }
    response = client.post("/posts", json=invalid_post)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_post_missing_required_fields(client):
    """Test creating a post with missing required fields"""
    invalid_post = {
        # Missing both title and content
        "published": True,
        "rating": 4,
    }
    response = client.post("/posts", json=invalid_post)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_post_id(client):
    """Test accessing post with invalid ID type"""
    response = client.get("/posts/invalid")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
