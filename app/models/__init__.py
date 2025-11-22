"""
SQLAlchemy models.
"""
from app.database import Base
from app.models.data_record import DataRecord

__all__ = ["Base", "DataRecord"]
