"""
Weather data fetching service using Open-Meteo API.
Open-Meteo is a free weather API that doesn't require an API key.
"""
import logging
from typing import List, Dict, Any
import httpx
from datetime import datetime
from app.config import TARGET_CITY, TARGET_LATITUDE, TARGET_LONGITUDE

logger = logging.getLogger(__name__)

OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_weather_data() -> List[Dict[str, Any]]:
    """
    Fetch current weather data from Open-Meteo API for Tel Aviv Yafo.

    Returns:
        List containing a single weather data record with temperature info

    Raises:
        Exception: If the API request fails
    """
    logger.info(f"Fetching weather data for {TARGET_CITY}")

    try:
        params = {
            "latitude": TARGET_LATITUDE,
            "longitude": TARGET_LONGITUDE,
            "current": "temperature_2m,weather_code",
            "timezone": "auto"
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPEN_METEO_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

        current = data.get("current", {})

        weather_record = {
            "source": "open-meteo",
            "city": TARGET_CITY,
            "timestamp": datetime.now().isoformat(),
            "temperature_c": current.get("temperature_2m"),
            "weather_description": current.get("weather_code")
        }

        logger.info(f"Weather data fetched successfully: {weather_record['temperature_c']}°C in {TARGET_CITY}")
        return [weather_record]

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching weather data: {str(e)}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}", exc_info=True)
        raise
