"""Script to execute migrations for the Islamic Knowledge Platform."""
import asyncio
import os
from pathlib import Path
from app.services.supabase_client import supabase
from app.data.regional_sample_data import REGIONAL_RULINGS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def execute_migrations():
    """Execute migrations and seed data."""
    try:
        # Create regional_rulings table
        logger.info("Creating regional_rulings table...")
        success = await supabase.create_table('regional_rulings')
        if not success:
            logger.error("Failed to create regional_rulings table")
            return False

        # Insert sample data
        logger.info("Inserting sample data...")
        for ruling in REGIONAL_RULINGS:
            try:
                result = await supabase.insert_content('regional_rulings', ruling)
                if result:
                    logger.info(f"Inserted ruling for topic: {ruling['topic']}")
                else:
                    logger.error(f"Failed to insert ruling for topic: {ruling['topic']}")
            except Exception as e:
                logger.error(f"Error inserting ruling: {str(e)}")

        logger.info("Migration completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error executing migrations: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(execute_migrations())
