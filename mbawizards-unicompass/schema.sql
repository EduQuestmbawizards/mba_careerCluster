-- =========================================================================
-- MBAWizards: Graduate Admissions & Career Intelligence Platform Supabase Schema
-- Table: career_students_data
-- Description: Consolidated table for candidate profile intake, 
--              assessments, GMAT/CAT/GRE scores, and AI roadmaps.
-- Safe to re-run multiple times (Idempotent Migration)
-- =========================================================================

-- 1. Create consolidated table if not exists
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Safely add any missing columns if table already existed previously
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS full_name TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS phone TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS city TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS country TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS nationality TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS education_level TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS field_of_study TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS target_university TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS target_country TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS target_field TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS career_interest TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS raw_form_data JSONB;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS generated_response TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS generated_html TEXT;
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now());
ALTER TABLE career_students_data ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now());

-- 3. Ensure unique index on email for on_conflict upserts
CREATE UNIQUE INDEX IF NOT EXISTS idx_career_students_email ON career_students_data(email);

-- 4. Enable Row Level Security (RLS)
ALTER TABLE career_students_data ENABLE ROW LEVEL SECURITY;

-- 5. Safe re-runnable policy for anon/service_role insert, select, and upsert
DO $$
BEGIN
    DROP POLICY IF EXISTS "Allow public insert and upsert" ON career_students_data;
    DROP POLICY IF EXISTS "Allow anon all operations" ON career_students_data;
END $$;

CREATE POLICY "Allow public insert and upsert" ON career_students_data
    FOR ALL
    TO anon, authenticated, service_role
    USING (true)
    WITH CHECK (true);
