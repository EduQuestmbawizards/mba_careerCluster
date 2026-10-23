-- =========================================================================
-- MBAWizards UniCompass: Supabase Database Schema
-- Table: career_students_data
-- Description: Consolidated table for candidate profile intake, 
--              4-pillar assessments, GMAT/CAT/GRE scores, and AI roadmaps.
-- =========================================================================

-- 1. Create consolidated table
CREATE TABLE IF NOT EXISTS career_students_data (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    full_name TEXT,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    city TEXT,
    country TEXT,
    nationality TEXT,
    education_level TEXT,
    field_of_study TEXT,
    target_university TEXT,
    target_country TEXT,
    target_field TEXT,
    career_interest TEXT,
    raw_form_data JSONB,
    generated_response TEXT,
    generated_html TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Fast search index on candidate email
CREATE INDEX IF NOT EXISTS idx_career_students_email ON career_students_data(email);

-- 3. Optional: Enable Row Level Security (RLS) and allow public inserts/upserts
ALTER TABLE career_students_data ENABLE ROW LEVEL SECURITY;

-- Allow anon and authenticated users to insert / upsert their intake records
CREATE POLICY "Allow public insert and upsert" ON career_students_data
    FOR ALL
    USING (true)
    WITH CHECK (true);
