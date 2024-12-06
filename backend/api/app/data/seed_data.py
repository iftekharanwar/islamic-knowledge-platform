from app.models.database import SessionLocal, IslamicContent, ContentType, Topic
from datetime import datetime

def seed_database():
    db = SessionLocal()

    # Sample Islamic content for testing
    content = [
        {
            "content_type": ContentType.QURAN,
            "topic": Topic.AQEEDAH,
            "title": "The Nature of Allah",
            "content": "Say, 'He is Allah, [who is] One, Allah, the Eternal Refuge. He neither begets nor is born, Nor is there to Him any equivalent.' (Surah Al-Ikhlas 112:1-4)",
            "source": "Quran",
            "reference": "Surah Al-Ikhlas",
            "scholar": None
        },
        {
            "content_type": ContentType.HADITH,
            "topic": Topic.FIQH,
            "title": "The Five Pillars of Islam",
            "content": "Islam has been built upon five things – on testifying that there is no god save Allah, and that Muhammad is His Messenger; on performing salah; on giving the zakah; on Hajj to the House; and on fasting during Ramadan.",
            "source": "Sahih al-Bukhari",
            "reference": "Hadith 8",
            "scholar": "Imam Bukhari"
        },
        {
            "content_type": ContentType.FATWA,
            "topic": Topic.FIQH,
            "title": "Digital Cryptocurrencies",
            "content": "The use of digital currencies must comply with Islamic principles of finance. They should have real value, be free from excessive uncertainty (gharar), and not involve usury (riba).",
            "source": "Contemporary Fatwa",
            "reference": "Islamic Fiqh Council",
            "scholar": "Contemporary Scholars"
        }
    ]

    try:
        for item in content:
            islamic_content = IslamicContent(**item)
            db.add(islamic_content)
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
