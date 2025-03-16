from collections import defaultdict
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel

from app.data_base import PostgresDB
from app.log_module import logger

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Root route
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Helo World"}


# Post routes
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    """Get all posts"""
    logger.info("Fetching all posts")
    with PostgresDB() as db:
        posts = db.execute_query("SELECT * FROM posts")
        logger.info(f"Retrieved {len(posts)} posts")
        return {"posts": posts}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    """Get a single post by ID"""
    logger.info(f"Fetching post with id: {id}")
    with PostgresDB() as db:
        post = db.execute_query("SELECT * FROM posts WHERE id = %s", (id,))
        if not post:
            logger.error(f"Post with id {id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found",
            )
        logger.info(f"Retrieved post:{post}")
        return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    """Create a new post"""
    logger.info(f"Creating new post: {post.dict()}")
    with PostgresDB() as db:
        new_post = db.execute_query(
            """
            INSERT INTO posts (title, content, published, rating)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (post.title, post.content, post.published, post.rating),
        )
        logger.info(f"Created new post")
        return {"post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete a post by ID"""
    logger.info(f"Attempting to delete post with id: {id}")
    with PostgresDB() as db:
        deleted_post = db.execute_query(
            "DELETE FROM posts WHERE id = %s RETURNING *", (id,)
        )
        if not deleted_post:
            logger.error(f"Post with id {id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found",
            )
        logger.info(f"Successfully deleted post: {deleted_post}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    """Update a post by ID"""
    logger.info(f"Attempting to update post {id} with data: {post.dict()}")
    with PostgresDB() as db:
        updated_post = db.execute_query(
            """
            UPDATE posts
            SET title = %s, content = %s, published = %s, rating = %s
            WHERE id = %s
            RETURNING *
            """,
            (post.title, post.content, post.published, post.rating, id),
        )

        if not updated_post:
            logger.error(f"Post with id {id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found",
            )
        logger.info(f"Successfully updated post: {updated_post}")
        return {"message": "post updated", "post": updated_post}
