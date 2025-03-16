import pytest

from app.data_base import PostgresDB


def test_database_connection():
    """Test database connection"""
    with PostgresDB() as db:
        result = db.execute_query("SELECT 1")
        assert result is not None


def test_database_query_execution():
    """Test query execution"""
    with PostgresDB() as db:
        # Create a test post
        result = db.execute_query(
            """
            INSERT INTO posts (title, content, published, rating)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            ("test title", "test content", True, 4),
        )
        assert result is not None
        assert len(result) == 1
        assert result[0]["title"] == "test title"
