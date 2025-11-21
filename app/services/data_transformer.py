"""
Data transformer service to convert aggregated data into database records.
"""
import json
from datetime import datetime
from typing import Dict, Any
from app.schemas.data_record import DataRecordCreate


def transform_aggregate_to_record(aggregate: Dict[str, Any]) -> DataRecordCreate:
    """
    Transform aggregated data into a DataRecordCreate schema for database insertion.

    Args:
        aggregate: Dictionary containing aggregated data from all sources

    Returns:
        DataRecordCreate instance ready for database insertion

    Raises:
        KeyError: If required data is missing from aggregate
    """
    # Extract weather data
    weather_data = aggregate["sources"]["weather"]["data"][0]
    city_name = weather_data["city"]
    current_temp = weather_data["temperature_c"]

    # Extract OSINT data
    osint_data = aggregate["sources"]["osint"]["data"]
    brand_name = osint_data["brand_name"]

    # Extract Gemini analysis results
    gemini_data = aggregate["sources"]["gemini"]
    sentiment_summary = gemini_data.get("sentiment_summary", "")
    news_summary = gemini_data.get("news_summary", "")

    # Convert raw responses to JSON strings
    raw_weather = json.dumps(aggregate["sources"]["weather"], ensure_ascii=False)
    raw_osint = json.dumps(aggregate["sources"]["osint"], ensure_ascii=False)
    raw_gemini_response = json.dumps(gemini_data, ensure_ascii=False) if gemini_data.get("status") == "success" else None

    # Create and return the record
    return DataRecordCreate(
        aggregation_timestamp_utc=datetime.utcnow(),
        city_name=city_name,
        current_temperature_c=current_temp,
        brand_name=brand_name,
        sentiment_summary=sentiment_summary,
        news_summary=news_summary,
        popularity_score=None,
        raw_weather_response=raw_weather,
        raw_osint_response=raw_osint,
        raw_gemini_response=raw_gemini_response
    )
