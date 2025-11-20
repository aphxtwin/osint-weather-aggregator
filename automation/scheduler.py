"""
Scheduler module for running periodic tasks.
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from app.services.aggregator import aggregate_all_data

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = AsyncIOScheduler()


async def run_data_aggregation_job():
    """
    Job that runs every 8 hours to aggregate weather and OSINT data.
    """
    try:
        logger.info(f"Starting scheduled data aggregation at {datetime.now()}")
        result = await aggregate_all_data()
        logger.info(f"Scheduled data aggregation completed successfully: {result}")
    except Exception as e:
        logger.error(f"Error during scheduled data aggregation: {str(e)}", exc_info=True)


def start_scheduler():
    """
    Initialize and start the scheduler with all periodic jobs.
    """
    if not scheduler.running:
        # Add job that runs every 8 hours
        scheduler.add_job(
            run_data_aggregation_job,
            trigger=IntervalTrigger(hours=8),
            id='data_aggregation_job',
            name='Aggregate weather and OSINT data',
            replace_existing=True,
            max_instances=1,  # Prevent concurrent runs
            coalesce=True,    # If multiple runs are missed, only run once
        )

        scheduler.start()
        logger.info("Scheduler started successfully - job will run every 8 hours")
    else:
        logger.warning("Scheduler is already running")


def stop_scheduler():
    """
    Gracefully shutdown the scheduler.
    """
    if scheduler.running:
        scheduler.shutdown(wait=True)
        logger.info("Scheduler stopped successfully")
    else:
        logger.warning("Scheduler is not running")


def get_scheduled_jobs():
    """
    Get information about all scheduled jobs.

    Returns:
        list: List of job information dictionaries
    """
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            'id': job.id,
            'name': job.name,
            'next_run': job.next_run_time,
            'trigger': str(job.trigger)
        })
    return jobs
