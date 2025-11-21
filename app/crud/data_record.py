"""
CRUD operations for data records.
"""
import logging
from sqlalchemy.orm import Session
from app.models.data_record import DataRecord
from app.schemas.data_record import DataRecordCreate

logger = logging.getLogger(__name__)


def create_data_record(db: Session, record: DataRecordCreate) -> DataRecord:
    """
    Create a new data record in the database.

    Args:
        db: Database session
        record: DataRecordCreate schema with record data (already transformed)

    Returns:
        Created DataRecord instance with auto-generated ID
    """
    db_record = DataRecord(
        aggregation_timestamp_utc=record.aggregation_timestamp_utc,
        city_name=record.city_name,
        current_temperature_c=record.current_temperature_c,
        brand_name=record.brand_name,
        sentiment_summary=record.sentiment_summary,
        news_summary=record.news_summary,
        popularity_score=record.popularity_score,
        raw_weather_response=record.raw_weather_response,
        raw_osint_response=record.raw_osint_response,
        raw_gemini_response=record.raw_gemini_response
    )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    logger.info(f"Created data record ID {db_record.id}: {record.city_name}, {record.brand_name}")
    return db_record
