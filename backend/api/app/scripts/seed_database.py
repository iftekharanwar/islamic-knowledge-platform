import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import Base, engine, SessionLocal, IslamicContent, ContentType, Topic
from app.data.initial_content import initial_content

def seed_database():
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")

        # Create database session
        db = SessionLocal()

        try:
            print("Seeding initial content...")
            # Create initial content
            for content_data in initial_content:
                content_type = ContentType(content_data["content_type"])
                topic = Topic(content_data["topic"])

                db_content = IslamicContent(
                    content_type=content_type,
                    topic=topic,
                    title=content_data["title"],
                    content=content_data["content"],
                    source=content_data["source"],
                    reference=content_data["reference"],
                    scholar=content_data.get("scholar")
                )
                db.add(db_content)
                print(f"Added content: {content_data['title']}")

            # Commit the changes
            db.commit()
            print("Successfully seeded database with initial content!")

        except Exception as e:
            print(f"Error seeding database: {e}")
            db.rollback()
            raise
        finally:
            db.close()

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    seed_database()
