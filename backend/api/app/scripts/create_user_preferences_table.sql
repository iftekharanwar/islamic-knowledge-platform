-- Create enum types for user preferences
CREATE TYPE madhab_type AS ENUM ('hanafi', 'shafii', 'maliki', 'hanbali');
CREATE TYPE learning_path_type AS ENUM ('basics', 'intermediate', 'advanced');

-- Create the user_preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    madhab madhab_type,
    language TEXT NOT NULL DEFAULT 'en',
    difficulty_level TEXT NOT NULL DEFAULT 'beginner',
    topics_of_interest TEXT[] DEFAULT ARRAY[]::TEXT[],
    learning_path learning_path_type,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_preferences_madhab ON user_preferences(madhab);
CREATE INDEX IF NOT EXISTS idx_user_preferences_learning_path ON user_preferences(learning_path);
