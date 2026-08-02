-- Optional manual init (app also runs SQLAlchemy create_all on startup)
-- docker compose exec postgres psql -U zhixue -d zhixue -f /dev/stdin < scripts/init_schema.sql

CREATE TABLE IF NOT EXISTS courses (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(64) PRIMARY KEY,
    course_id VARCHAR(64) NOT NULL,
    media_key VARCHAR(512) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    progress DOUBLE PRECISION NOT NULL DEFAULT 0,
    result TEXT,
    error_msg TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_jobs_course_id ON jobs (course_id);
