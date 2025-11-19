-- Add referral fields to users table
ALTER TABLE users 
ADD COLUMN referral_code VARCHAR(20) UNIQUE,
ADD COLUMN referred_by VARCHAR(36),
ADD COLUMN coins INT DEFAULT 0;

-- Create index on referral_code for faster lookups
CREATE INDEX idx_referral_code ON users(referral_code);
CREATE INDEX idx_referred_by ON users(referred_by);
