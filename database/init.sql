-- ShalaConnect Database Setup
-- Run this ONLY if you want to pre-create the database manually.
-- Otherwise Spring Boot (ddl-auto=update) will create tables automatically.

CREATE DATABASE IF NOT EXISTS school_management
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE school_management;

-- The tables are auto-created by Hibernate on first run.
-- The default admin account is also seeded automatically:
--   Email:    admin@shalaconnect.in
--   Password: Admin@123
--
-- Change the admin password immediately after first login!
