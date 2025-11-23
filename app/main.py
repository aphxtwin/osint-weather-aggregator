"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.api.endpoints import router
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting OSINT Weather Aggregator application...")

    # Initialize database
    init_db()
    logger.info("Database initialized")
    logger.info("Daily automation managed by n8n - see README for setup")

    yield

    # Shutdown
    logger.info("Shutting down application...")


app = FastAPI(
    title="OSINT Weather Aggregator",
    description="API for aggregating weather data from multiple OSINT sources",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OSINT Weather Aggregator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "automation": "n8n (external)"
    }
