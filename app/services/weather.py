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

# WMO Weather interpretation codes
WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


def get_weather_description(code: int) -> str:
    """Convert WMO weather code to description."""
    return WEATHER_CODE_MAP.get(code, f"Unknown ({code})")


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
        weather_code = current.get("weather_code")

        weather_record = {
            "source": "open-meteo",
            "city": TARGET_CITY,
            "timestamp": datetime.now().isoformat(),
            "temperature_c": current.get("temperature_2m"),
            "weather_description": get_weather_description(weather_code) if weather_code is not None else "Unknown"
        }

        logger.info(f"Weather data fetched successfully: {weather_record['temperature_c']}°C in {TARGET_CITY}")
        return [weather_record]

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching weather data: {str(e)}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}", exc_info=True)
        raise
