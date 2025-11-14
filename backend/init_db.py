"""
Database initialization script.
Creates the database and user if they don't exist.
"""
import os
import sys
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_database():
    """
    Create the MySQL database and user if they don't exist.
    This should be run with a MySQL user that has CREATE DATABASE privileges.
    """
    # Database configuration
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', 3306))
    db_name = os.getenv('DB_NAME', 'airzone')
    db_user = os.getenv('DB_USER', 'airzone_user')
    db_password = os.getenv('DB_PASSWORD', '')
    
    # Root credentials for initial setup
    root_user = os.getenv('DB_ROOT_USER', 'root')
    root_password = os.getenv('DB_ROOT_PASSWORD', '')
    
    try:
        # Connect to MySQL server (without specifying database)
        print(f"Connecting to MySQL server at {db_host}:{db_port}...")
        connection = pymysql.connect(
            host=db_host,
            port=db_port,
            user=root_user,
            password=root_password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            print(f"Creating database '{db_name}' if it doesn't exist...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Database '{db_name}' is ready")
            
            # Create user if it doesn't exist (MySQL 8.0+ syntax)
            print(f"Creating user '{db_user}' if it doesn't exist...")
            try:
                cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'")
                cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}'")
                print(f"✓ User '{db_user}' is ready")
            except pymysql.err.OperationalError as e:
                if "Operation CREATE USER failed" in str(e):
                    print(f"⚠ User '{db_user}' already exists")
                else:
                    raise
            
            # Grant privileges
            print(f"Granting privileges to '{db_user}' on database '{db_name}'...")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'%'")
            cursor.execute("FLUSH PRIVILEGES")
            print(f"✓ Privileges granted to '{db_user}'")
        
        connection.commit()
        print("\n✓ Database initialization completed successfully!")
        print(f"\nDatabase: {db_name}")
        print(f"User: {db_user}")
        print(f"Host: {db_host}:{db_port}")
        
    except pymysql.err.OperationalError as e:
        print(f"\n✗ Error connecting to MySQL: {e}")
        print("\nPlease ensure:")
        print("1. MySQL server is running")
        print("2. Root credentials are correct in .env file:")
        print("   DB_ROOT_USER=root")
        print("   DB_ROOT_PASSWORD=your_root_password")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during database initialization: {e}")
        sys.exit(1)
    finally:
        if 'connection' in locals():
            connection.close()


if __name__ == '__main__':
    print("=" * 60)
    print("Airzone Database Initialization")
    print("=" * 60)
    print()
    create_database()
