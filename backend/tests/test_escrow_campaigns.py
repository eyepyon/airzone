#!/usr/bin/env python3
"""
Test script to check escrow_campaigns table
"""
import sys
from sqlalchemy import create_engine, text
from config import Config

def test_escrow_campaigns():
    """Test if escrow_campaigns table exists and can be queried"""
    try:
        # Create engine
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        
        # Test connection
        with engine.connect() as conn:
            print("✓ Database connection successful")
            
            # Check if table exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = 'escrow_campaigns'
            """))
            
            table_exists = result.fetchone()[0] > 0
            
            if table_exists:
                print("✓ escrow_campaigns table exists")
                
                # Try to query the table
                result = conn.execute(text("""
                    SELECT * FROM escrow_campaigns 
                    WHERE is_active = TRUE 
                    AND start_date <= NOW() 
                    AND end_date >= NOW()
                    ORDER BY created_at DESC
                """))
                
                campaigns = result.fetchall()
                print(f"✓ Query successful - Found {len(campaigns)} campaigns")
                
                for campaign in campaigns:
                    print(f"  - {campaign[1]}: {campaign[2][:50]}...")
                
                return True
            else:
                print("✗ escrow_campaigns table does NOT exist")
                print("\nPlease run the migration:")
                print("  mysql -u root -p airzone < backend/database/migrations/add_escrow_campaigns.sql")
                return False
                
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_escrow_campaigns()
    sys.exit(0 if success else 1)
