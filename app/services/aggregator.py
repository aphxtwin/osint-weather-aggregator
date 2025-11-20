"""
Data aggregation service that collects weather data from multiple sources.
"""
import logging
from datetime import datetime
from typing import Dict, Any
from app.services.weather import fetch_weather_data
from app.services.osint import fetch_osint_data

logger = logging.getLogger(__name__)


async def aggregate_all_data() -> Dict[str, Any]:
    """
    Aggregate weather and OSINT data from all configured sources.

    Returns:
        Dict containing aggregation results and statistics
    """
    start_time = datetime.now()
    results = {
        "timestamp": start_time.isoformat(),
        "sources": {},
        "success_count": 0,
        "error_count": 0,
        "total_records": 0
    }

    logger.info("Starting data aggregation from all sources...")

    # Fetch weather data
    try:
        weather_data = await fetch_weather_data()
        results["sources"]["weather"] = {
            "status": "success",
            "records": len(weather_data) if weather_data else 0
        }
        results["success_count"] += 1
        results["total_records"] += len(weather_data) if weather_data else 0

        logger.info(f"Weather data fetched successfully: {len(weather_data) if weather_data else 0} records")
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}", exc_info=True)
        results["sources"]["weather"] = {
            "status": "error",
            "error": str(e)
        }
        results["error_count"] += 1

    # Fetch OSINT data
    try:
        osint_data = await fetch_osint_data()
        results["sources"]["osint"] = {
            "status": "success",
            "records": len(osint_data) if osint_data else 0
        }
        results["success_count"] += 1
        results["total_records"] += len(osint_data) if osint_data else 0

        logger.info(f"OSINT data fetched successfully: {len(osint_data) if osint_data else 0} records")
    except Exception as e:
        logger.error(f"Error fetching OSINT data: {str(e)}", exc_info=True)
        results["sources"]["osint"] = {
            "status": "error",
            "error": str(e)
        }
        results["error_count"] += 1

    end_time = datetime.now()
    results["duration_seconds"] = (end_time - start_time).total_seconds()

    logger.info(f"Data aggregation completed: {results['success_count']} sources successful, "
                f"{results['error_count']} errors, {results['total_records']} total records")

    return results
