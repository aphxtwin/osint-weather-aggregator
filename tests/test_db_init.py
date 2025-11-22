"""
Test database initialization.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import init_db
from app.models import DataRecord

print("Initializing database...")
init_db()
print("✓ Database initialized successfully!")
print(f"✓ DataRecord model loaded: {DataRecord.__tablename__}")