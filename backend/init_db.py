"""
Database initialization script.
Creates all tables defined in the models.
"""
import os
import sys
from sqlalchemy import create_engine
from config import config
from models import Base

# Import all models to ensure they are registered with Base
from models import (
    User, Wallet, NFTMint, Product, Order, OrderItem,
    Payment, WiFiSession, TaskQueue
)


def init_database(env='development'):
    """
    Initialize the database by creating all tables.
    
    Args:
        env (str): Environment name (development, production, testing)
    """
    # Get configuration
    app_config = config.get(env, config['default'])
    
    # Create engine
    engine = create_engine(
        app_config.SQLALCHEMY_DATABASE_URI,
        echo=app_config.SQLALCHEMY_ECHO
    )
    
    print(f"Initializing database for environment: {env}")
    print(f"Database URI: {app_config.SQLALCHEMY_DATABASE_URI}")
    
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        print("✓ All tables created successfully!")
        
        # Print created tables
        print("\nCreated tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"✗ Error creating tables: {str(e)}")
        sys.exit(1)
    finally:
        engine.dispose()


def drop_database(env='development'):
    """
    Drop all tables from the database.
    WARNING: This will delete all data!
    
    Args:
        env (str): Environment name (development, production, testing)
    """
    # Get configuration
    app_config = config.get(env, config['default'])
    
    # Create engine
    engine = create_engine(
        app_config.SQLALCHEMY_DATABASE_URI,
        echo=app_config.SQLALCHEMY_ECHO
    )
    
    print(f"WARNING: Dropping all tables for environment: {env}")
    print(f"Database URI: {app_config.SQLALCHEMY_DATABASE_URI}")
    
    response = input("Are you sure you want to drop all tables? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    try:
        # Drop all tables
        Base.metadata.drop_all(engine)
        print("✓ All tables dropped successfully!")
        
    except Exception as e:
        print(f"✗ Error dropping tables: {str(e)}")
        sys.exit(1)
    finally:
        engine.dispose()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Database initialization script')
    parser.add_argument(
        '--env',
        type=str,
        default='development',
        choices=['development', 'production', 'testing'],
        help='Environment name'
    )
    parser.add_argument(
        '--drop',
        action='store_true',
        help='Drop all tables before creating (WARNING: deletes all data)'
    )
    
    args = parser.parse_args()
    
    if args.drop:
        drop_database(args.env)
    
    init_database(args.env)
