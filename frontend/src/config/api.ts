const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  KNOWLEDGE_BASE: {
    QUERY: `${API_BASE_URL}/api/v1/knowledge/search`,
  },
  SCHOLARS: {
    PROFILE: `${API_BASE_URL}/api/v1/scholars/profile`,
    REGISTER: `${API_BASE_URL}/api/v1/scholars/register`,
    CONTRIBUTIONS: `${API_BASE_URL}/api/v1/scholars/contributions`,
    REVIEWS: `${API_BASE_URL}/api/v1/scholars/reviews`,
  },
};

export default API_ENDPOINTS;
