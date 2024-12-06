import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.ai_service import ai_service

async def test_ai_service():
    """Test the AI service's ability to handle various Islamic topics."""
    test_queries = [
        # Test Aqeedah knowledge
        "What is the Islamic concept of Allah's oneness?",

        # Test Fiqh knowledge
        "What are the five pillars of Islam?",

        # Test contemporary issues
        "What is the Islamic perspective on cryptocurrency?",
    ]

    print("\nTesting AI Service Response Generation...")
    print("----------------------------------------")

    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = await ai_service.generate_response(query)

            print("\nResponse:")
            print(f"Answer: {response['response']}")
            print(f"Confidence: {response['confidence']:.2f}")

            print("\nReferences:")
            for ref in response['references']:
                print(f"- Type: {ref['type']}")
                print(f"  Source: {ref['source']}")
                print(f"  Reference: {ref['reference']}")
                if ref.get('scholar'):
                    print(f"  Scholar: {ref['scholar']}")

            print("\nRelevance Assessment:")
            if response['confidence'] > 0.7:
                print("✓ High confidence response")
            elif response['confidence'] > 0.5:
                print("△ Moderate confidence response")
            else:
                print("✗ Low confidence response")

        except Exception as e:
            print(f"Error testing query: {str(e)}")

        print("\n" + "-"*40)

if __name__ == "__main__":
    asyncio.run(test_ai_service())
