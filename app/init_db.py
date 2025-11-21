"""
Database initialization script.
Run this to create all database tables.
"""
import logging
from app.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Creating database tables...")
    init_db()
    logger.info("Database tables created successfully!")
