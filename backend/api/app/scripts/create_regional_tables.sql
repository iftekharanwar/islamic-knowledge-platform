-- Create enum type for regions
CREATE TYPE region_type AS ENUM (
    'middle_east',
    'south_asia',
    'southeast_asia',
    'africa',
    'europe',
    'north_america',
    'australia'
);

-- Create table for regional rulings
CREATE TABLE IF NOT EXISTS regional_rulings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    region region_type NOT NULL,
    topic TEXT NOT NULL,
    ruling TEXT NOT NULL,
    context TEXT NOT NULL,
    scholars TEXT[] NOT NULL,
    references TEXT[] NOT NULL,
    cultural_notes TEXT,
    local_practices TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX idx_regional_rulings_region ON regional_rulings(region);
CREATE INDEX idx_regional_rulings_topic ON regional_rulings(topic);
CREATE INDEX idx_regional_rulings_search ON regional_rulings USING GIN (to_tsvector('english', ruling || ' ' || context || ' ' || cultural_notes));
