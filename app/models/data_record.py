"""
SQLAlchemy model for data records.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from app.database import Base


class DataRecord(Base):
    """Store one record per day with aggregated weather and OSINT data."""
    __tablename__ = "data_records"

    id = Column(Integer, primary_key=True, index=True)
    aggregation_timestamp_utc = Column(DateTime, nullable=False, default=datetime.utcnow)
    city_name = Column(String(100), nullable=False)
    current_temperature_c = Column(Float, nullable=False)
    brand_name = Column(String(100), nullable=False)
    sentiment_summary = Column(Text, nullable=False)
    news_summary = Column(Text, nullable=False)
    popularity_score = Column(Float, nullable=True)
    raw_weather_response = Column(Text, nullable=False)  # JSON string
    raw_osint_response = Column(Text, nullable=False)  # JSON string
    raw_gemini_response = Column(Text, nullable=True)  # JSON string (optional)