-- Airzone Database Setup SQL Script
-- Run this script with a MySQL user that has CREATE DATABASE privileges
-- Example: mysql -u root -p < setup_database.sql

-- Create database
CREATE DATABASE IF NOT EXISTS airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (if it doesn't exist)
-- Note: Replace 'your_secure_password' with your actual password
CREATE USER IF NOT EXISTS 'airzone_user'@'localhost' IDENTIFIED BY 'your_secure_password';
CREATE USER IF NOT EXISTS 'airzone_user'@'%' IDENTIFIED BY 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'%';

-- Apply privileges
FLUSH PRIVILEGES;

-- Confirm setup
SELECT 'Database and user created successfully!' AS Status;
