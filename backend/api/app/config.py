from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql+psycopg2://postgres:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxld3NhcGttdW10aHhrc3BzZW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzMyNTIsImV4cCI6MjA0ODk0OTI1Mn0.tnYFIgUGwFi4hLGsQrWeeZkSeX6uKWKh5eU8VZT13NQ@db.lewsapkmumthxkspsemo.supabase.co:5432/postgres"

    # AI Model settings
    AI_MODEL_PATH: str = "models/islamic_knowledge_model"

    # API settings
    API_V1_PREFIX: str = "/api/v1"

    # Authentication settings
    JWT_SECRET_KEY: str = "your-secret-key-here"  # Change in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Offline sync settings
    OFFLINE_CACHE_SIZE: int = 1000  # Number of entries to cache

    class Config:
        env_file = ".env"

settings = Settings()
