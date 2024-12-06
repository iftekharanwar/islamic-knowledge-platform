import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine
from app.config import settings

def test_connection():
    try:
        # Create engine with explicit parameters
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            echo=True  # Enable SQL logging
        )

        # Try to connect
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
