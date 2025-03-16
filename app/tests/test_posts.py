import pytest
from fastapi import status


def test_get_all_posts(client):
    """Test getting all posts"""
    response = client.get("/posts")
    assert (
        response.status_code == status.HTTP_200_OK
    ), "Failed to get posts with 200 status"
    assert "posts" in response.json(), "Response missing 'posts' key"
    assert isinstance(
        response.json()["posts"], list
    ), "Posts should be returned as a list"


def test_get_one_post(client, test_post):
    """Test getting a single post"""
    # First create a post
    create_response = client.post("/posts", json=test_post)
    assert (
        create_response.status_code == status.HTTP_201_CREATED
    ), "Failed to create test post"

    # Get all posts and find the first one
    response = client.get("/posts")
    posts = response.json()["posts"]
    assert posts, "No posts found after creation"

    first_post = posts[0]
    post_id = first_post["id"]

    # Get this specific post
    response = client.get(f"/posts/{post_id}")
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Failed to get post with id {post_id}"
    returned_post = response.json()["post"]
    assert (
        returned_post["title"] == test_post["title"]
    ), "Returned post title doesn't match created post"
    assert (
        returned_post["content"] == test_post["content"]
    ), "Returned post content doesn't match created post"


def test_get_non_existent_post(client):
    """Test getting a post that doesn't exist"""
    response = client.get("/posts/99999")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Should return 404 for non-existent post"


def test_create_post(client, test_post):
    """Test creating a post"""
    response = client.post("/posts", json=test_post)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), "Failed to create post with 201 status"

    created_post = response.json()["post"]
    if isinstance(created_post, list):
        created_post = created_post[0]

    assert (
        created_post["title"] == test_post["title"]
    ), "Created post title doesn't match input"
    assert (
        created_post["content"] == test_post["content"]
    ), "Created post content doesn't match input"
    assert "id" in created_post, "Created post missing ID field"


def test_delete_post(client, test_post):
    """Test deleting a post"""
    create_response = client.post("/posts", json=test_post)
    assert (
        create_response.status_code == status.HTTP_201_CREATED
    ), "Failed to create test post"

    response = client.get("/posts")
    posts = response.json()["posts"]
    assert posts, "No posts found after creation"

    post_id = posts[0]["id"]
    delete_response = client.delete(f"/posts/{post_id}")
    assert (
        delete_response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Failed to delete post {post_id}"

    get_response = client.get(f"/posts/{post_id}")
    assert (
        get_response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Post {post_id} still exists after deletion"


def test_delete_non_existent_post(client):
    """Test deleting a post that doesn't exist"""
    response = client.delete("/posts/99999")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Should return 404 when deleting non-existent post"


def test_update_post(client, test_post):
    """Test updating a post"""
    create_response = client.post("/posts", json=test_post)
    assert (
        create_response.status_code == status.HTTP_201_CREATED
    ), "Failed to create test post"

    response = client.get("/posts")
    posts = response.json()["posts"]
    assert posts, "No posts found after creation"

    post_id = posts[0]["id"]
    updated_data = test_post.copy()
    updated_data["title"] = "updated title"

    update_response = client.put(f"/posts/{post_id}", json=updated_data)
    assert (
        update_response.status_code == status.HTTP_200_OK
    ), f"Failed to update post {post_id}"

    get_response = client.get(f"/posts/{post_id}")
    assert (
        get_response.status_code == status.HTTP_200_OK
    ), f"Failed to get updated post {post_id}"
    updated_post = get_response.json()["post"]
    assert (
        updated_post["title"] == "updated title"
    ), "Post title was not updated correctly"


def test_update_non_existent_post(client, test_post):
    """Test updating a post that doesn't exist"""
    response = client.put("/posts/99999", json=test_post)
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Should return 404 when updating non-existent post"
