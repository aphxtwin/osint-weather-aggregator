"""
API endpoints for the OSINT Weather Aggregator.
"""
from fastapi import APIRouter
from app.services.aggregator import aggregate_all_data

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
