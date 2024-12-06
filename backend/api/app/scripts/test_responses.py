import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.ai_service import AIService

async def test_responses():
    ai_service = AIService()

    test_queries = [
        "What are the rules for prayer during travel?",
        "What is the significance of Ramadan?",
        "What is the nature of Allah in Islam?",
        "What are the five pillars of Islam?",
        "What is the Islamic view on cryptocurrencies?"
    ]

    print("\nTesting AI responses across various Islamic topics...")
    print("=" * 80)

    for query in test_queries:
        print(f"\nQuery: {query}")
        response = await ai_service.get_response(query)
        print(f"Response: {response['answer']}")
        print(f"Confidence: {response['confidence']}")
        print(f"References: {response['references']}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(test_responses())
