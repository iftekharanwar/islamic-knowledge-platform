from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.services.supabase_client import supabase
import re

class AIService:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.content_cache = {}
        self.embedding_cache = {}

    async def initialize(self):
        await self._load_content()

    async def _load_content(self):
        try:
            result = await supabase.get_content('islamic_content')
            self.content_cache = {item['id']: item for item in result}

            for content_id, content in self.content_cache.items():
                text = f"{content['title']} {content['content']}"
                self.embedding_cache[content_id] = self.model.encode(text)

            print(f"Loaded {len(self.content_cache)} Islamic texts and generated embeddings")
        except Exception as e:
            print(f"Error loading content: {str(e)}")
            raise

    def _preprocess_query(self, query: str) -> str:
        islamic_terms = {
            r'\b(salah|salat|prayer)\b': 'salah',
            r'\b(zakat|zakah)\b': 'zakat',
            r'\b(hajj|pilgrimage)\b': 'hajj',
            r'\b(sawm|siyam|fasting)\b': 'sawm',
            r'\b(quran|koran)\b': 'quran',
            r'\b(hadith|hadeeth)\b': 'hadith'
        }

        processed_query = query.lower()
        for pattern, replacement in islamic_terms.items():
            processed_query = re.sub(pattern, replacement, processed_query, flags=re.IGNORECASE)

        return processed_query

    def _validate_content_authenticity(self, content: Dict) -> bool:
        required_fields = ['source', 'reference', 'scholar']
        if not all(field in content for field in required_fields):
            return False

        authentic_sources = {
            'quran': ['sahih_international', 'pickthall', 'yusuf_ali'],
            'hadith': ['bukhari', 'muslim', 'abu_dawood', 'tirmidhi', 'nasai', 'ibn_majah'],
            'fatwa': ['dar_al_ifta', 'permanent_committee', 'azhar']
        }

        content_type = content.get('content_type', '').lower()
        source = content.get('source', '').lower()

        if content_type in authentic_sources:
            return any(auth_source in source for auth_source in authentic_sources[content_type])

        return False

    def _check_content_bias(self, content: Dict) -> float:
        bias_score = 1.0
        content_text = (content.get('title', '') + ' ' + content.get('content', '')).lower()

        sectarian_terms = ['only true', 'only correct', 'false sect', 'deviant']
        if any(term in content_text for term in sectarian_terms):
            bias_score *= 0.5

        extreme_indicators = ['forbidden', 'mandatory', 'must', 'always', 'never']
        extreme_count = sum(1 for term in extreme_indicators if term in content_text)
        if extreme_count > 2:
            bias_score *= 0.7

        balanced_indicators = ['scholars differ', 'difference of opinion', 'majority view', 'some scholars']
        if any(term in content_text for term in balanced_indicators):
            bias_score *= 1.2

        return bias_score

    def find_relevant_content(self, query: str, top_k: int = 3, preferences: Dict = None) -> List[Dict]:
        try:
            processed_query = self._preprocess_query(query)
            query_embedding = self.model.encode(processed_query)

            similarities = []
            for content_id, content_embedding in self.embedding_cache.items():
                content = self.content_cache[content_id]

                if not self._validate_content_authenticity(content):
                    continue

                base_score = cosine_similarity(
                    [query_embedding],
                    [content_embedding]
                )[0][0]

                bias_score = self._check_content_bias(content)

                madhab_score = 1.0
                if preferences and preferences.get('madhab'):
                    content_text = (content.get('title', '') + ' ' + content.get('content', '')).lower()
                    user_madhab = preferences['madhab'].lower()

                    if user_madhab in content_text:
                        madhab_score = 1.5
                    elif 'general' in content_text:
                        madhab_score = 1.2
                    else:
                        other_madhabs = {'hanafi', 'shafii', 'maliki', 'hanbali'} - {user_madhab}
                        if any(madhab in content_text for madhab in other_madhabs):
                            madhab_score = 0.5

                learning_path_score = 1.0
                if preferences and preferences.get('learning_path'):
                    content_difficulty = content.get('difficulty_level', 'intermediate').lower()
                    user_path = preferences['learning_path'].lower()

                    path_mapping = {
                        'basics': ['beginner', 'basic'],
                        'intermediate': ['intermediate'],
                        'advanced': ['advanced', 'scholarly']
                    }

                    if content_difficulty in path_mapping.get(user_path, []):
                        learning_path_score = 1.3

                query_terms = set(processed_query.split())
                content_terms = set((content['title'] + ' ' + content['content']).lower().split())
                term_overlap = len(query_terms.intersection(content_terms))
                term_score = 1.0 + (0.1 * term_overlap) if term_overlap > 0 else 1.0

                final_score = base_score * madhab_score * learning_path_score * term_score * bias_score
                similarities.append((content_id, final_score))

            similarities.sort(key=lambda x: x[1], reverse=True)
            results = []
            for content_id, score in similarities[:top_k]:
                content = self.content_cache[content_id]
                results.append({
                    **content,
                    'relevance_score': float(score)
                })

            return results
        except Exception as e:
            print(f"Error finding relevant content: {str(e)}")
            return []

    async def get_response(self, query: str) -> Dict:
        if not self.content_cache:
            await self.initialize()
            if not self.content_cache:
                print("Warning: Content cache is still empty after initialization")
        return await self.generate_response(query)

    async def generate_response(self, query: str, context: List[Dict] = None, preferences: Dict = None) -> Dict:
        try:
            if not self.content_cache:
                await self.initialize()

            if any(term in query.lower() for term in ['hack', 'attack', 'harm', 'kill', 'destroy']):
                return {
                    "answer": "I apologize, but I cannot provide information about harmful or unethical actions. Please ask questions that align with Islamic principles of peace and benefit.",
                    "confidence": 0.0,
                    "references": []
                }

            region = preferences.get('region') if preferences else None

            relevant_content = context if context else self.find_relevant_content(
                query,
                top_k=5,
                preferences=preferences
            )

            if region:
                try:
                    regional_query = f"""
                    SELECT * FROM regional_rulings
                    WHERE region = '{region}'
                    AND (topic ILIKE '%{query}%' OR ruling ILIKE '%{query}%')
                    LIMIT 3
                    """
                    regional_content = await supabase.execute_sql(regional_query)
                    if regional_content:
                        for content in regional_content:
                            relevant_content.append({
                                'content': f"In {region}, {content['ruling']}. {content.get('cultural_notes', '')}",
                                'source': 'Regional Ruling',
                                'reference': content.get('references', []),
                                'scholar': content.get('scholars', []),
                                'relevance_score': 1.0
                            })
                except Exception as e:
                    print(f"Error fetching regional content: {e}")

            if not relevant_content:
                return {
                    "answer": "I apologize, but I couldn't find specific information to answer your question accurately. Please rephrase or ask about a different Islamic topic.",
                    "confidence": 0.0,
                    "references": []
                }

            answer_parts = []
            total_confidence = 0.0
            references = []

            for idx, content in enumerate(relevant_content):
                confidence = content.get('relevance_score', 0.0)
                if confidence < 0.1:
                    continue

                content_text = content.get('content', '')
                if idx == 0:
                    answer_parts.append(content_text)
                else:
                    if len(content_text) > 20:
                        answer_parts.append(content_text)

                total_confidence += confidence
                ref = {
                    "type": content.get('content_type', ''),
                    "source": content.get('source', ''),
                    "reference": content.get('reference', ''),
                    "scholar": content.get('scholar', '')
                }
                if ref not in references:
                    references.append(ref)

            final_answer = ' '.join(answer_parts)
            avg_confidence = min(100.0, (total_confidence / len(relevant_content)) * 200) if relevant_content else 0.0

            sensitive_topics = ['jihad', 'war', 'politics', 'sectarian']
            if any(topic in query.lower() for topic in sensitive_topics):
                final_answer = f"Note: This is a sensitive topic that requires careful understanding and proper context. Please consult with qualified scholars for detailed guidance. {final_answer}"

            return {
                "answer": final_answer,
                "confidence": round(avg_confidence, 1),
                "references": references,
                "source_type": relevant_content[0].get('content_type') if relevant_content else None,
                "verified": all(self._validate_content_authenticity(content) for content in relevant_content)
            }
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return {
                "answer": "I apologize, but I encountered an error while processing your question about Islamic knowledge.",
                "confidence": 0.0,
                "references": []
            }

# Create a singleton instance
ai_service = AIService()
