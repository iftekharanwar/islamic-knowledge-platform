-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create user_preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    madhab TEXT,
    language TEXT NOT NULL DEFAULT 'en',
    difficulty_level TEXT NOT NULL DEFAULT 'beginner',
    topics_of_interest TEXT[] DEFAULT '{}',
    learning_path TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_preferences_madhab ON user_preferences(madhab);
CREATE INDEX IF NOT EXISTS idx_user_preferences_language ON user_preferences(language);


-- Create trigger for updating updated_at timestamp
CREATE TRIGGER update_user_preferences_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
