"""
Simple database setup script - runs migrations only.
Use this after manually creating the database and user.

Prerequisites:
1. Database 'airzone' exists
2. User 'airzone_user' exists with proper privileges
3. Credentials are set in .env file
"""
import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()


def check_connection():
    """Check if we can connect to the database."""
    try:
        import pymysql
        
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'airzone_user'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'airzone'),
            charset='utf8mb4'
        )
        connection.close()
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease ensure:")
        print("1. Database 'airzone' exists")
        print("2. User 'airzone_user' has proper privileges")
        print("3. Credentials in .env are correct")
        return False


def run_migrations():
    """Run Alembic migrations."""
    print("\nRunning database migrations...")
    try:
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print("✓ Migrations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Migration failed: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print("✗ Alembic not found. Install with: pip install alembic")
        return False


def seed_data():
    """Seed initial data."""
    print("\nSeeding initial data...")
    seed_script = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'seed_data.py')
    
    if not os.path.exists(seed_script):
        print("⚠ Seed script not found, skipping...")
        return True
    
    try:
        result = subprocess.run(
            [sys.executable, seed_script],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print("✓ Data seeding completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠ Seeding failed (optional): {e}")
        return True  # Non-critical


def main():
    print("=" * 60)
    print("Airzone Database Setup (Simple)")
    print("=" * 60)
    print()
    print("This script will:")
    print("  1. Check database connection")
    print("  2. Run migrations to create tables")
    print("  3. Seed initial data (optional)")
    print()
    print("Prerequisites:")
    print("  - Database 'airzone' must exist")
    print("  - User 'airzone_user' must exist")
    print("  - Credentials must be set in .env")
    print()
    
    # Check connection
    if not check_connection():
        print("\n" + "=" * 60)
        print("Setup Instructions:")
        print("=" * 60)
        print()
        print("Run this SQL to create database and user:")
        print("  mysql -u your_admin_user -p < backend/setup_database.sql")
        print()
        print("Or manually:")
        print("  CREATE DATABASE airzone;")
        print("  CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'password';")
        print("  GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';")
        print()
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("\nYou can try running manually:")
        print("  cd backend")
        print("  alembic upgrade head")
        sys.exit(1)
    
    # Seed data
    seed_data()
    
    # Success
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Start backend: cd backend && python app.py")
    print("  2. Start frontend: cd frontend && npm run dev")
    print()


if __name__ == '__main__':
    main()
