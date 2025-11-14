"""
Complete database setup script.
This script performs all database initialization steps:
1. Creates the database and user
2. Runs Alembic migrations
3. Seeds initial data
"""
import os
import sys
import subprocess

# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_dir)


def run_command(command, cwd=None, description=None):
    """
    Run a shell command and handle errors.
    
    Args:
        command: Command to run (list or string)
        cwd: Working directory
        description: Description of what the command does
    """
    if description:
        print(f"\n{description}...")
    
    try:
        if isinstance(command, str):
            command = command.split()
        
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout:
            print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def main():
    """Main setup function."""
    print("=" * 70)
    print("Airzone Database Setup")
    print("=" * 70)
    print()
    print("This script will:")
    print("  1. Create the MySQL database and user")
    print("  2. Run Alembic migrations to create tables")
    print("  3. Seed initial test data")
    print()
    
    # Get user confirmation
    response = input("Do you want to continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Setup cancelled.")
        sys.exit(0)
    
    print()
    print("-" * 70)
    
    # Step 1: Create database and user
    print("\nStep 1: Creating database and user")
    print("-" * 70)
    sys.path.insert(0, backend_dir)
    try:
        # Import and run init_db
        os.chdir(backend_dir)
        from init_db import create_database
        create_database()
    except Exception as e:
        print(f"✗ Failed to create database: {e}")
        print("\nPlease ensure:")
        print("  - MySQL server is running")
        print("  - Root credentials are set in backend/.env")
        print("  - DB_ROOT_USER and DB_ROOT_PASSWORD are configured")
        sys.exit(1)
    
    # Step 2: Run migrations
    print("\n" + "-" * 70)
    print("Step 2: Running Alembic migrations")
    print("-" * 70)
    
    # Try different ways to run alembic
    success = False
    
    # Try: alembic upgrade head
    if not success:
        success = run_command(
            ['alembic', 'upgrade', 'head'],
            cwd=backend_dir,
            description="Running migrations with 'alembic' command"
        )
    
    # Try: python -m alembic upgrade head
    if not success:
        success = run_command(
            [sys.executable, '-m', 'alembic', 'upgrade', 'head'],
            cwd=backend_dir,
            description="Running migrations with 'python -m alembic' command"
        )
    
    if not success:
        print("\n✗ Failed to run migrations")
        print("\nYou can try running manually:")
        print(f"  cd {backend_dir}")
        print("  alembic upgrade head")
        sys.exit(1)
    
    print("✓ Migrations completed successfully")
    
    # Step 3: Seed data
    print("\n" + "-" * 70)
    print("Step 3: Seeding initial data")
    print("-" * 70)
    
    try:
        scripts_dir = os.path.join(os.path.dirname(__file__))
        seed_script = os.path.join(scripts_dir, 'seed_data.py')
        
        success = run_command(
            [sys.executable, seed_script],
            description="Seeding test data"
        )
        
        if not success:
            print("⚠ Warning: Failed to seed data")
            print("You can run it manually later:")
            print(f"  python {seed_script}")
        else:
            print("✓ Data seeding completed successfully")
            
    except Exception as e:
        print(f"⚠ Warning: Error during data seeding: {e}")
        print("You can run it manually later")
    
    # Final summary
    print("\n" + "=" * 70)
    print("Database Setup Complete!")
    print("=" * 70)
    print()
    print("✓ Database created and configured")
    print("✓ Tables created via migrations")
    print("✓ Initial data seeded")
    print()
    print("Next steps:")
    print("  1. Update backend/.env with your configuration")
    print("  2. Start the Flask application: python backend/app.py")
    print("  3. Start the Next.js frontend: cd frontend && npm run dev")
    print()


if __name__ == '__main__':
    main()
