import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';
import { ScholarProfile, ScholarContribution, PeerReview } from '../types/scholar';

interface QueryPreferences {
  language?: string;
  difficultyLevel?: string;
}

interface QueryResponse {
  text: string;
  confidence: number;
  references: {
    type: string;
    source: string;
    reference: string;
    scholar?: string;
  }[];
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Knowledge Base
export const queryKnowledgeBase = async (
  query: string,
  preferences?: QueryPreferences
): Promise<QueryResponse> => {
  try {
    const response = await api.post(API_ENDPOINTS.KNOWLEDGE_BASE.QUERY, {
      query,
      ...preferences,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.message || 'Failed to query knowledge base');
    }
    throw error;
  }
};

// Scholar Profile
export const getScholarProfile = async (): Promise<ScholarProfile> => {
  const response = await api.get(API_ENDPOINTS.SCHOLARS.PROFILE);
  return response.data;
};

export const registerScholar = async (data: {
  name: string;
  email: string;
  credentials: string;
  institution?: string;
  specializations: string[];
}): Promise<ScholarProfile> => {
  const response = await api.post(API_ENDPOINTS.SCHOLARS.REGISTER, data);
  return response.data;
};

// Contributions
export const submitContribution = async (data: {
  type: string;
  content: string;
  references: string;
  scholarId: string;
}): Promise<ScholarContribution> => {
  const response = await api.post(API_ENDPOINTS.SCHOLARS.CONTRIBUTIONS, data);
  return response.data;
};

export const getContributionsForReview = async (): Promise<ScholarContribution[]> => {
  const response = await api.get(`${API_ENDPOINTS.SCHOLARS.CONTRIBUTIONS}/review`);
  return response.data;
};

export const getScholarContributions = async (scholarId: string): Promise<ScholarContribution[]> => {
  const response = await api.get(`${API_ENDPOINTS.SCHOLARS.CONTRIBUTIONS}/${scholarId}`);
  return response.data;
};

// Reviews
export const submitReview = async (data: {
  contributionId: string;
  reviewerId: string;
  status: string;
  comment: string;
}): Promise<PeerReview> => {
  const response = await api.post(API_ENDPOINTS.SCHOLARS.REVIEWS, data);
  return response.data;
};

export const getContributionReviews = async (contributionId: string): Promise<PeerReview[]> => {
  const response = await api.get(`${API_ENDPOINTS.SCHOLARS.REVIEWS}/${contributionId}`);
  return response.data;
};
