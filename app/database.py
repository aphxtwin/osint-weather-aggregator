"""
Database connection and session management.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import DATABASE_URL

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={},
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependency function to get database session.

    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    """
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")