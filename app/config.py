"""
Application configuration.
"""
import os

# Target location - Tel Aviv Yafo
TARGET_CITY = os.getenv("TARGET_CITY", "Tel Aviv Yafo")
TARGET_LATITUDE = os.getenv("TARGET_LATITUDE", "32.0853")
TARGET_LONGITUDE = os.getenv("TARGET_LONGITUDE", "34.7818")

# Target brand
TARGET_BRAND = os.getenv("TARGET_BRAND", "Gymshark")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://osint_user:osint_password@postgres:5432/osint_weather")

# Application settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Reddit OSINT settings
REDDIT_SEARCH_QUERY = os.getenv("REDDIT_SEARCH_QUERY", "gymshark")
REDDIT_SEARCH_LIMIT = int(os.getenv("REDDIT_SEARCH_LIMIT", "10"))
REDDIT_SEARCH_SORT = os.getenv("REDDIT_SEARCH_SORT", "new")