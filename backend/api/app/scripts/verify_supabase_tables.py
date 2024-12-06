"""Script to verify Supabase database tables and structure."""
import asyncio
from app.services.supabase_client import supabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_tables():
    """Verify database tables and their structure."""
    try:
        # Try to query the regional_rulings table
        result = supabase.client.table('regional_rulings').select("*").limit(1).execute()
        logger.info("regional_rulings table exists and is queryable")
        logger.info(f"Sample data: {result.data if result.data else 'No data'}")

        # Try to insert test data
        test_data = {
            "region": "test_region",
            "topic": "test_topic",
            "ruling": "test_ruling",
            "context": "test_context",
            "scholars": ["test_scholar"],
            "references": ["test_reference"],
            "cultural_notes": "test_notes",
            "local_practices": "test_practices"
        }

        insert_result = await supabase.insert_content('regional_rulings', test_data)
        if insert_result:
            logger.info("Successfully inserted test data")
            logger.info(f"Inserted data: {insert_result}")

            # Clean up test data
            delete_result = await supabase.delete_content('regional_rulings', {"topic": "test_topic"})
            logger.info(f"Cleanup result: {delete_result}")
        else:
            logger.error("Failed to insert test data")

    except Exception as e:
        logger.error(f"Error verifying tables: {str(e)}")
        raise e

if __name__ == "__main__":
    asyncio.run(verify_tables())
