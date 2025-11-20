#!/usr/bin/env python
"""
Test auth service wallet creation
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def test_database_connection():
    """Test database connection and check wallets"""
    print("Testing database connection...")
    print("-" * 50)
    
    try:
        # Get database URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("✗ DATABASE_URL not set in .env")
            return False
        
        print(f"Database URL: {database_url.split('@')[1] if '@' in database_url else 'N/A'}")
        
        # Create engine
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("✓ Database connected")
        
        # Check users
        result = session.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        print(f"✓ Users table: {user_count} users")
        
        # Check wallets
        result = session.execute(text("SELECT COUNT(*) FROM wallets"))
        wallet_count = result.scalar()
        print(f"✓ Wallets table: {wallet_count} wallets")
        
        # Get recent wallets
        result = session.execute(text(
            "SELECT id, user_id, address, created_at FROM wallets "
            "ORDER BY created_at DESC LIMIT 5"
        ))
        wallets = result.fetchall()
        
        if wallets:
            print("\nRecent wallets:")
            for wallet in wallets:
                print(f"  ID: {wallet[0]}")
                print(f"  User ID: {wallet[1]}")
                print(f"  Address: {wallet[2]}")
                print(f"  Created: {wallet[3]}")
                print()
        else:
            print("\n⚠ No wallets found in database")
            print("This means wallets are not being created during user registration")
        
        session.close()
        
        print("-" * 50)
        print("✓ Database test completed")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_database_connection()
    sys.exit(0 if success else 1)
