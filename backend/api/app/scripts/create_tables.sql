-- Create enum types for content categories
CREATE TYPE content_type AS ENUM ('quran', 'hadith', 'fatwa');
CREATE TYPE topic_type AS ENUM ('aqeedah', 'fiqh', 'tafsir', 'seerah', 'general');

-- Create the islamic_content table
CREATE TABLE IF NOT EXISTS islamic_content (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    content_type content_type NOT NULL,
    topic topic_type NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    reference TEXT,
    scholar TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better search performance
CREATE INDEX IF NOT EXISTS idx_content_type ON islamic_content(content_type);
CREATE INDEX IF NOT EXISTS idx_topic ON islamic_content(topic);
CREATE INDEX IF NOT EXISTS idx_content_search ON islamic_content USING GIN (to_tsvector('english', content));
CREATE INDEX IF NOT EXISTS idx_title_search ON islamic_content USING GIN (to_tsvector('english', title));

-- Function to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to update timestamp
CREATE TRIGGER update_islamic_content_updated_at
    BEFORE UPDATE ON islamic_content
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
