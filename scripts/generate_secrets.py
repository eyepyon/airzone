#!/usr/bin/env python3
"""
Script to generate secure secret keys for production deployment.
This script generates cryptographically secure random keys for:
- Flask SECRET_KEY
- JWT_SECRET_KEY
- ENCRYPTION_KEY (for wallet private keys)
"""

import secrets
import string
import sys


def generate_secret_key(length=64):
    """Generate a cryptographically secure random key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_hex_key(length=32):
    """Generate a hex-encoded random key (for encryption)"""
    return secrets.token_hex(length)


def main():
    print("=" * 70)
    print("Airzone Production Secret Key Generator")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANT: Store these keys securely!")
    print("   - Never commit these to version control")
    print("   - Use environment variables or secure secret management")
    print("   - Keep backups in a secure location")
    print()
    print("-" * 70)
    
    # Generate Flask SECRET_KEY
    flask_secret = generate_secret_key(64)
    print("Flask SECRET_KEY:")
    print(f"SECRET_KEY={flask_secret}")
    print()
    
    # Generate JWT SECRET_KEY
    jwt_secret = generate_secret_key(64)
    print("JWT SECRET_KEY:")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print()
    
    # Generate ENCRYPTION_KEY (for wallet private keys)
    encryption_key = generate_hex_key(32)  # 32 bytes = 256 bits
    print("ENCRYPTION_KEY (for wallet private keys):")
    print(f"ENCRYPTION_KEY={encryption_key}")
    print()
    
    print("-" * 70)
    print()
    print("📝 Next Steps:")
    print("1. Copy these keys to your production .env file")
    print("2. Update backend/.env with these values")
    print("3. Ensure the .env file has restricted permissions (chmod 600)")
    print("4. Never share or commit these keys")
    print()
    print("=" * 70)


if __name__ == '__main__':
    main()
