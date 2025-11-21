"""
Pydantic schemas for data records (API contract).
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DataRecordCreate(BaseModel):
    """Schema for creating a new data record."""
    aggregation_timestamp_utc: datetime
    city_name: str
    current_temperature_c: float
    brand_name: str
    sentiment_summary: str
    news_summary: str
    popularity_score: Optional[float] = None
    raw_weather_response: str  # JSON string
    raw_osint_response: str  # JSON string
    raw_gemini_response: Optional[str] = None  # JSON string (optional)


class DataRecordRead(BaseModel):
    """Schema for reading a data record."""
    id: int
    aggregation_timestamp_utc: datetime
    city_name: str
    current_temperature_c: float
    brand_name: str
    sentiment_summary: str
    news_summary: str
    popularity_score: Optional[float] = None
    raw_weather_response: str  # JSON string
    raw_osint_response: str  # JSON string
    raw_gemini_response: Optional[str] = None  # JSON string (optional)

    model_config = ConfigDict(from_attributes=True)


class DataRecordReadLatest(BaseModel):
    """Schema for reading latest data record (excludes raw fields)."""
    id: int
    aggregation_timestamp_utc: datetime
    city_name: str
    current_temperature_c: float
    brand_name: str
    sentiment_summary: str
    news_summary: str
    popularity_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)