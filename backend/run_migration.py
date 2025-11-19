#!/usr/bin/env python3
"""
Run database migration to add referral fields to users table.
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Run the migration."""
    try:
        # Get database URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("Error: DATABASE_URL not found in environment variables")
            sys.exit(1)
        
        print(f"Connecting to database...")
        engine = create_engine(database_url)
        
        # Read migration SQL
        migration_file = 'database/migrations/add_referral_fields_to_users.sql'
        print(f"Reading migration file: {migration_file}")
        
        with open(migration_file, 'r') as f:
            sql = f.read()
        
        # Execute migration
        print("Executing migration...")
        with engine.connect() as conn:
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in sql.split(';') if s.strip()]
            for statement in statements:
                print(f"Executing: {statement[:50]}...")
                conn.execute(text(statement))
            conn.commit()
        
        print("✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == '__main__':
    success = run_migration()
    sys.exit(0 if success else 1)
