"""
Application configuration.
"""
import os

# Target location - Tel Aviv Yafo
TARGET_CITY = os.getenv("TARGET_CITY", "Tel Aviv Yafo")
TARGET_LATITUDE = os.getenv("TARGET_LATITUDE", "32.0853")
TARGET_LONGITUDE = os.getenv("TARGET_LONGITUDE", "34.7818")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# Application settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Reddit OSINT settings
REDDIT_SEARCH_QUERY = "gymshark"
REDDIT_SEARCH_LIMIT = 10
REDDIT_SEARCH_SORT = "new"