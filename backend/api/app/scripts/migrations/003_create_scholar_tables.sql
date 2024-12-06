-- Create enum types for scholar-related tables
CREATE TYPE verification_status AS ENUM ('pending', 'verified', 'rejected');
CREATE TYPE specialization AS ENUM ('fiqh', 'hadith', 'tafsir', 'aqeedah', 'seerah', 'general');
CREATE TYPE contribution_status AS ENUM ('pending', 'approved', 'rejected');
CREATE TYPE review_status AS ENUM ('approved', 'rejected', 'needs_revision');

-- Create table for scholar profiles
CREATE TABLE IF NOT EXISTS scholar_profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    credentials TEXT NOT NULL,
    institution TEXT,
    specializations specialization[] NOT NULL,
    verification_status verification_status NOT NULL DEFAULT 'pending',
    verification_date TIMESTAMPTZ,
    verified_by UUID REFERENCES scholar_profiles(id),
    contributions_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create table for scholar contributions
CREATE TABLE IF NOT EXISTS scholar_contributions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    scholar_id UUID NOT NULL REFERENCES scholar_profiles(id),
    content_id UUID NOT NULL,
    contribution_type TEXT NOT NULL,
    content TEXT NOT NULL,
    status contribution_status NOT NULL DEFAULT 'pending',
    review_count INTEGER DEFAULT 0,
    approved_by UUID[] DEFAULT '{}',
    rejected_by UUID[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create table for peer reviews
CREATE TABLE IF NOT EXISTS peer_reviews (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    contribution_id UUID NOT NULL REFERENCES scholar_contributions(id),
    reviewer_id UUID NOT NULL REFERENCES scholar_profiles(id),
    review_type TEXT NOT NULL,
    comment TEXT NOT NULL,
    status review_status NOT NULL DEFAULT 'needs_revision',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(contribution_id, reviewer_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_scholar_verification ON scholar_profiles(verification_status);
CREATE INDEX idx_scholar_specializations ON scholar_profiles USING GIN (specializations);
CREATE INDEX idx_contribution_status ON scholar_contributions(status);
CREATE INDEX idx_contribution_scholar ON scholar_contributions(scholar_id);
CREATE INDEX idx_review_contribution ON peer_reviews(contribution_id);
CREATE INDEX idx_review_reviewer ON peer_reviews(reviewer_id);

-- Add trigger for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_scholar_profiles_timestamp
    BEFORE UPDATE ON scholar_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scholar_contributions_timestamp
    BEFORE UPDATE ON scholar_contributions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_peer_reviews_timestamp
    BEFORE UPDATE ON peer_reviews
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
