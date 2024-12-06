-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create regional_rulings table
CREATE TABLE IF NOT EXISTS regional_rulings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    region TEXT NOT NULL,
    topic TEXT NOT NULL,
    ruling TEXT NOT NULL,
    context TEXT NOT NULL,
    scholars TEXT[] DEFAULT '{}',
    references TEXT[] DEFAULT '{}',
    cultural_notes TEXT,
    local_practices TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_regional_rulings_region ON regional_rulings(region);
CREATE INDEX IF NOT EXISTS idx_regional_rulings_topic ON regional_rulings(topic);

-- Create trigger for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_regional_rulings_updated_at
    BEFORE UPDATE ON regional_rulings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
