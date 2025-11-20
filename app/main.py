"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.api.endpoints import router
from automation.scheduler import start_scheduler, stop_scheduler, get_scheduled_jobs

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

    # Start scheduler
    start_scheduler()
    logger.info("Scheduler started - jobs will run every 8 hours")

    # Log scheduled jobs
    jobs = get_scheduled_jobs()
    for job in jobs:
        logger.info(f"Scheduled job: {job['name']} (ID: {job['id']}) - Next run: {job['next_run']}")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    stop_scheduler()
    logger.info("Scheduler stopped")


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
    jobs = get_scheduled_jobs()
    return {
        "status": "healthy",
        "scheduler": {
            "active": len(jobs) > 0,
            "jobs": jobs
        }
    }
