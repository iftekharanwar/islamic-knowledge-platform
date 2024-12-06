export interface ScholarProfile {
  id: string;
  name: string;
  email: string;
  credentials: string;
  institution?: string;
  specializations: string[];
  verification_status: 'pending' | 'verified' | 'rejected';
  verification_date?: string;
  verified_by?: string;
  contributions_count: number;
  created_at: string;
  updated_at: string;
}

export interface ScholarContribution {
  id: string;
  scholar_id: string;
  scholar_name: string;
  content_id: string;
  contribution_type: string;
  content: string;
  status: string;
  review_count: number;
  approved_by: string[];
  rejected_by: string[];
  created_at: string;
  updated_at: string;
}

export interface PeerReview {
  id: string;
  contribution_id: string;
  reviewer_id: string;
  review_type: string;
  comment: string;
  status: string;
  created_at: string;
  updated_at: string;
}
