-- Create regional_rulings table
CREATE TABLE IF NOT EXISTS regional_rulings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
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
