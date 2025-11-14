#!/bin/bash
# Quick Database Setup Script for Airzone
# This script automates the entire database setup process

set -e  # Exit on error

echo "=========================================="
echo "Airzone Database Quick Setup"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if MySQL is running
if ! command -v mysql &> /dev/null; then
    echo "Warning: MySQL client not found in PATH"
    echo "Please ensure MySQL server is running"
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "Error: backend/.env file not found"
    echo "Please create it from backend/.env.example"
    echo ""
    echo "  cp backend/.env.example backend/.env"
    echo "  # Then edit backend/.env with your settings"
    exit 1
fi

echo "Prerequisites check passed!"
echo ""

# Run the setup script
echo "Running automated setup..."
python scripts/setup_database.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Verify setup: cd backend && python verify_database.py"
    echo "  2. Start backend: cd backend && python app.py"
    echo "  3. Start frontend: cd frontend && npm run dev"
    echo ""
else
    echo ""
    echo "Setup failed. Please check the error messages above."
    echo "For help, see: backend/DATABASE_SETUP.md"
    exit 1
fi
