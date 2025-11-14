"""
Database verification script.
Checks if the database is properly set up with all tables and initial data.
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from config import config
from models import User, Wallet, NFTMint, Product, Order, OrderItem, Payment, WiFiSession, TaskQueue

# Load environment variables
load_dotenv()


def verify_database():
    """Verify database setup and contents."""
    print("=" * 70)
    print("Airzone Database Verification")
    print("=" * 70)
    print()
    
    try:
        # Get database connection
        env = os.getenv('FLASK_ENV', 'development')
        db_url = config[env].SQLALCHEMY_DATABASE_URI
        
        print(f"Environment: {env}")
        print(f"Database URL: {db_url.split('@')[1] if '@' in db_url else 'N/A'}")
        print()
        
        # Create engine and session
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test connection
        print("Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        print("✓ Database connection successful")
        print()
        
        # Check tables
        print("Checking database tables...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'users',
            'wallets',
            'nft_mints',
            'products',
            'orders',
            'order_items',
            'payments',
            'wifi_sessions',
            'task_queue',
            'alembic_version'
        ]
        
        missing_tables = []
        for table in expected_tables:
            if table in tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ {table} (MISSING)")
                missing_tables.append(table)
        
        if missing_tables:
            print()
            print(f"✗ Missing {len(missing_tables)} table(s)")
            print("Run migrations: cd backend && alembic upgrade head")
            return False
        
        print()
        print("✓ All tables exist")
        print()
        
        # Check migration version
        print("Checking migration version...")
        try:
            result = session.execute(text("SELECT version_num FROM alembic_version"))
            version = result.fetchone()
            if version:
                print(f"  Current version: {version[0]}")
                print("  ✓ Migrations have been applied")
            else:
                print("  ⚠ No migration version found")
        except Exception as e:
            print(f"  ⚠ Could not check migration version: {e}")
        
        print()
        
        # Check data counts
        print("Checking data counts...")
        
        models = [
            ('Users', User),
            ('Wallets', Wallet),
            ('NFT Mints', NFTMint),
            ('Products', Product),
            ('Orders', Order),
            ('Order Items', OrderItem),
            ('Payments', Payment),
            ('WiFi Sessions', WiFiSession),
            ('Task Queue', TaskQueue),
        ]
        
        for name, model in models:
            count = session.query(model).count()
            print(f"  {name}: {count}")
        
        print()
        
        # Check if products are seeded
        product_count = session.query(Product).count()
        if product_count > 0:
            print("✓ Database contains seeded data")
            print()
            print("Sample products:")
            products = session.query(Product).limit(3).all()
            for product in products:
                nft_required = "NFT Required" if product.required_nft_id else "Public"
                print(f"  - {product.name} (¥{product.price:,}) [{nft_required}]")
        else:
            print("⚠ No products found in database")
            print("Run seed script: python scripts/seed_data.py")
        
        print()
        print("=" * 70)
        print("Database Verification Complete!")
        print("=" * 70)
        print()
        print("✓ Database is properly configured and ready to use")
        print()
        
        session.close()
        return True
        
    except Exception as e:
        print(f"\n✗ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Please ensure:")
        print("  1. MySQL server is running")
        print("  2. Database credentials are correct in backend/.env")
        print("  3. Database has been initialized: python backend/init_db.py")
        print("  4. Migrations have been run: cd backend && alembic upgrade head")
        return False


if __name__ == '__main__':
    success = verify_database()
    sys.exit(0 if success else 1)
