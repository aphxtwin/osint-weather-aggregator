"""
Data aggregation service that collects weather data from multiple sources.
"""
import logging
from datetime import datetime
from typing import Dict, Any
from app.services.weather import fetch_weather_data
from app.services.osint import fetch_osint_data
from app.services.gemini import analyze_sentiment, analyze_trends
from app.services.data_transformer import transform_aggregate_to_record
from app.database import SessionLocal
from app.crud.data_record import create_data_record

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
            "records": len(weather_data) if weather_data else 0,
            "data": weather_data
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
    osint_data = None
    try:
        osint_data = await fetch_osint_data()
        results["sources"]["osint"] = {
            "status": "success",
            "records": len(osint_data) if osint_data else 0,
            "data": osint_data
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

    # Analyze OSINT data with Gemini (if OSINT data was successfully fetched)
    if osint_data and len(osint_data.get("posts", [])) > 0:
        try:
            # Format OSINT posts for Gemini analysis
            osint_text = "\n\n".join([
                f"Post {i+1}:\nTitle: {post.get('title', '')}\nText: {post.get('text', '')}"
                for i, post in enumerate(osint_data["posts"])
            ])

            # Analyze sentiment
            sentiment_summary = analyze_sentiment(osint_text)

            # Analyze trends
            news_summary = analyze_trends(osint_text)

            results["sources"]["gemini"] = {
                "status": "success",
                "sentiment_summary": sentiment_summary,
                "news_summary": news_summary
            }
            results["success_count"] += 1

            logger.info("Gemini analysis completed successfully")
        except Exception as e:
            logger.error(f"Error analyzing with Gemini: {str(e)}", exc_info=True)
            results["sources"]["gemini"] = {
                "status": "error",
                "error": str(e)
            }
            results["error_count"] += 1
    else:
        logger.warning("Skipping Gemini analysis - no OSINT data available")
        results["sources"]["gemini"] = {
            "status": "skipped",
            "reason": "No OSINT data available"
        }

    end_time = datetime.now()
    results["duration_seconds"] = (end_time - start_time).total_seconds()

    logger.info(f"Data aggregation completed: {results['success_count']} sources successful, "
                f"{results['error_count']} errors, {results['total_records']} total records")

    # Transform aggregated data into database record format and save to database
    transformed_record = None
    db_record_id = None
    if results["success_count"] >= 2:  # Need at least weather and OSINT data
        try:
            transformed_record = transform_aggregate_to_record(results)
            logger.info(f"Data transformed successfully for database insertion: {transformed_record.city_name}, {transformed_record.brand_name}")

            # Save to database
            db = SessionLocal()
            try:
                db_record = create_data_record(db, transformed_record)
                db_record_id = db_record.id
                logger.info(f"Successfully saved record to database with ID: {db_record_id}")
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error transforming or saving data: {str(e)}", exc_info=True)

    # Add transformed record to results for inspection
    results["transformed_record"] = transformed_record.dict() if transformed_record else None
    results["db_record_id"] = db_record_id

    return results
