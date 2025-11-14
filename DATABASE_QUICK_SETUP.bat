@echo off
REM Airzone Database Quick Setup Script for Windows
REM This script automates the database setup process

echo ====================================================================
echo Airzone Database Quick Setup
echo ====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if MySQL is running
echo Checking if MySQL is running...
sc query MySQL80 | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] MySQL service is not running
    echo Attempting to start MySQL...
    net start MySQL80 >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to start MySQL
        echo Please start MySQL manually and try again
        pause
        exit /b 1
    )
    echo [OK] MySQL started successfully
) else (
    echo [OK] MySQL is running
)
echo.

REM Check if .env file exists
if not exist "backend\.env" (
    echo [WARNING] backend\.env file not found
    echo Creating from .env.example...
    copy "backend\.env.example" "backend\.env" >nul
    echo.
    echo [ACTION REQUIRED] Please edit backend\.env and set:
    echo   - DB_ROOT_PASSWORD (your MySQL root password)
    echo   - DB_PASSWORD (password for airzone_user)
    echo.
    echo Press any key after updating backend\.env...
    pause >nul
)

echo [OK] Environment file exists
echo.

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r backend\requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
) else (
    echo [OK] Dependencies installed
)
echo.

REM Run the setup script
echo ====================================================================
echo Running database setup...
echo ====================================================================
echo.

python scripts\setup_database.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo [ERROR] Database setup failed
    echo ====================================================================
    echo.
    echo Please check the error messages above and:
    echo   1. Ensure MySQL is running
    echo   2. Verify credentials in backend\.env
    echo   3. Check that root user has CREATE DATABASE privileges
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo Running database verification...
echo ====================================================================
echo.

python backend\verify_database.py

if errorlevel 1 (
    echo.
    echo [WARNING] Verification found some issues
    echo Please review the output above
) else (
    echo.
    echo ====================================================================
    echo SUCCESS! Database is ready to use
    echo ====================================================================
    echo.
    echo Next steps:
    echo   1. Start the backend:  cd backend ^&^& python app.py
    echo   2. Start the frontend: cd frontend ^&^& npm run dev
    echo   3. Visit http://localhost:3000
)

echo.
pause
