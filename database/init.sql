-- ShalaConnect Database Initialization (PostgreSQL 16)
-- Automatically executed when the PostgreSQL container boots for the first time.

-- Enable cryptographic and UUID extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set session timezone to Indian Standard Time (IST)
SET timezone = 'Asia/Kolkata';

-- JPA/Hibernate automatically creates and validates all 13 application tables on startup:
--   users, schools, attendance_records, gr_documents, gr_document_seen,
--   meetings, meeting_acknowledgments, events, event_implementations,
--   event_impl_photos, dynamic_forms, form_responses, notifications.

-- Default Cluster Administrator credentials seeded by DataSeeder.java:
--   Email:    admin@shalaconnect.in
--   Password: Admin@123
