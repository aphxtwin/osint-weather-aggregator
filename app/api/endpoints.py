"""
API endpoints for the OSINT Weather Aggregator.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.aggregator import aggregate_all_data
from app.database import get_db
from app.models.data_record import DataRecord
from app.schemas.data_record import DataRecordReadLatest

router = APIRouter()


@router.post("/aggregate")
async def trigger_aggregation():
    """
    Manually trigger data aggregation from all sources.

    Returns:
        Dict containing aggregation results and statistics
    """
    results = await aggregate_all_data()
    return results


@router.get("/status")
async def get_status():
    """
    Get the current status of the aggregator service.

    Returns:
        Dict containing service status information
    """
    return {
        "status": "operational",
        "message": "OSINT Weather Aggregator is running"
    }


@router.get("/data/latest", response_model=DataRecordReadLatest)
async def get_latest_data(db: Session = Depends(get_db)):
    """
    Get the most recent data record (excludes raw API responses).

    Returns:
        Latest data record without raw fields

    Raises:
        HTTPException: 404 if no data records exist
    """
    latest_record = db.query(DataRecord).order_by(
        DataRecord.aggregation_timestamp_utc.desc()
    ).first()

    if not latest_record:
        raise HTTPException(status_code=404, detail="No data records found")

    return latest_record
