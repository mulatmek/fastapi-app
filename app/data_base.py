import psycopg2
from psycopg2.extras import RealDictCursor

from app.log_module import logger


class PostgresDB:
    def __init__(
        self,
        database="postgres",
        host="localhost",
        user="postgres",
        password="postgres11",
    ):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor,
            )
            self.cursor = self.conn.cursor()
            logger.info("Database connection was successful!")
        except Exception as error:
            logger.error(f"Connecting to database failed: {str(error)}")
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            logger.debug(f"Executing query: {query}")
            if "RETURNING" in query.strip().upper() or query.strip().upper().startswith(
                "SELECT"
            ):
                result = self.cursor.fetchall()
                self.conn.commit()
                logger.debug(f"Query returned {len(result)} results")
                return result
            self.conn.commit()
            logger.debug("Query executed successfully")
            return None
        except Exception as error:
            logger.error(f"Query execution failed: {str(error)}")
            raise

    def execute_many(self, query, params_list):
        """Execute multiple similar queries"""
        try:
            self.cursor.executemany(query, params_list)
            self.conn.commit()
            logger.debug(f"Executed batch query with {len(params_list)} parameters")
        except Exception as error:
            logger.error(f"Batch query execution failed: {str(error)}")
            raise
