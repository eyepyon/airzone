#!/bin/bash
# ============================================================================
# Systemd Services Setup Script for Airzone
# ============================================================================
#
# This script automates the systemd service setup for Airzone backend and frontend.
# It should be run with sudo privileges.
#
# Usage: sudo bash setup_services.sh
#
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run as root (use sudo)"
    exit 1
fi

print_info "Starting systemd services setup for Airzone..."
echo ""

# ============================================================================
# 1. Check Prerequisites
# ============================================================================

print_step "Checking prerequisites..."

# Check if service files exist
if [ ! -f "airzone-backend.service" ]; then
    print_error "airzone-backend.service not found in current directory"
    exit 1
fi

if [ ! -f "airzone-frontend.service" ]; then
    print_error "airzone-frontend.service not found in current directory"
    exit 1
fi

# Check if application directories exist
if [ ! -d "/var/www/airzone/backend" ]; then
    print_error "Backend directory not found: /var/www/airzone/backend"
    exit 1
fi

if [ ! -d "/var/www/airzone/frontend" ]; then
    print_error "Frontend directory not found: /var/www/airzone/frontend"
    exit 1
fi

print_info "Prerequisites check passed"
echo ""

# ============================================================================
# 2. Create Log Directory
# ============================================================================

print_step "Creating log directory..."

mkdir -p /var/log/airzone
chown www-data:www-data /var/log/airzone
chmod 755 /var/log/airzone

print_info "Log directory created: /var/log/airzone"
echo ""

# ============================================================================
# 3. Install Gunicorn (if not already installed)
# ============================================================================

print_step "Checking Gunicorn installation..."

if [ ! -f "/var/www/airzone/backend/venv/bin/gunicorn" ]; then
    print_warning "Gunicorn not found. Installing..."
    
    # Activate virtual environment and install gunicorn
    cd /var/www/airzone/backend
    source venv/bin/activate
    pip install gunicorn
    deactivate
    
    print_info "Gunicorn installed"
else
    print_info "Gunicorn already installed"
fi

echo ""

# ============================================================================
# 4. Build Frontend (if not already built)
# ============================================================================

print_step "Checking frontend build..."

if [ ! -f "/var/www/airzone/frontend/.next/BUILD_ID" ]; then
    print_warning "Frontend not built. Building..."
    
    cd /var/www/airzone/frontend
    sudo -u www-data npm run build
    
    print_info "Frontend built successfully"
else
    print_info "Frontend already built"
fi

echo ""

# ============================================================================
# 5. Install Service Files
# ============================================================================

print_step "Installing systemd service files..."

# Backup existing services if they exist
if [ -f "/etc/systemd/system/airzone-backend.service" ]; then
    print_warning "Backing up existing backend service..."
    cp /etc/systemd/system/airzone-backend.service \
       /etc/systemd/system/airzone-backend.service.backup.$(date +%Y%m%d_%H%M%S)
fi

if [ -f "/etc/systemd/system/airzone-frontend.service" ]; then
    print_warning "Backing up existing frontend service..."
    cp /etc/systemd/system/airzone-frontend.service \
       /etc/systemd/system/airzone-frontend.service.backup.$(date +%Y%m%d_%H%M%S)
fi

# Copy service files
cp airzone-backend.service /etc/systemd/system/
cp airzone-frontend.service /etc/systemd/system/

# Set permissions
chmod 644 /etc/systemd/system/airzone-backend.service
chmod 644 /etc/systemd/system/airzone-frontend.service

print_info "Service files installed"
echo ""

# ============================================================================
# 6. Reload Systemd
# ============================================================================

print_step "Reloading systemd daemon..."

systemctl daemon-reload

print_info "Systemd daemon reloaded"
echo ""

# ============================================================================
# 7. Enable Services
# ============================================================================

print_step "Enabling services to start on boot..."

systemctl enable airzone-backend.service
systemctl enable airzone-frontend.service

print_info "Services enabled"
echo ""

# ============================================================================
# 8. Start Services
# ============================================================================

print_step "Starting services..."

# Stop services if already running
systemctl stop airzone-backend.service 2>/dev/null || true
systemctl stop airzone-frontend.service 2>/dev/null || true

# Start backend
print_info "Starting backend service..."
systemctl start airzone-backend.service

# Wait a moment for backend to start
sleep 3

# Check backend status
if systemctl is-active --quiet airzone-backend.service; then
    print_info "Backend service started successfully"
else
    print_error "Backend service failed to start"
    print_info "Checking logs..."
    journalctl -u airzone-backend.service -n 20 --no-pager
    exit 1
fi

# Start frontend
print_info "Starting frontend service..."
systemctl start airzone-frontend.service

# Wait a moment for frontend to start
sleep 3

# Check frontend status
if systemctl is-active --quiet airzone-frontend.service; then
    print_info "Frontend service started successfully"
else
    print_error "Frontend service failed to start"
    print_info "Checking logs..."
    journalctl -u airzone-frontend.service -n 20 --no-pager
    exit 1
fi

echo ""

# ============================================================================
# 9. Display Status
# ============================================================================

print_info "Setup completed successfully!"
echo ""
echo "=========================================================================="
echo "Service Status"
echo "=========================================================================="
echo ""

print_info "Backend Service:"
systemctl status airzone-backend.service --no-pager -l | head -n 15
echo ""

print_info "Frontend Service:"
systemctl status airzone-frontend.service --no-pager -l | head -n 15
echo ""

echo "=========================================================================="
echo "Useful Commands"
echo "=========================================================================="
echo ""
echo "View backend logs:"
echo "  sudo journalctl -u airzone-backend.service -f"
echo ""
echo "View frontend logs:"
echo "  sudo journalctl -u airzone-frontend.service -f"
echo ""
echo "Restart services:"
echo "  sudo systemctl restart airzone-backend"
echo "  sudo systemctl restart airzone-frontend"
echo ""
echo "Stop services:"
echo "  sudo systemctl stop airzone-backend"
echo "  sudo systemctl stop airzone-frontend"
echo ""
echo "Check service status:"
echo "  sudo systemctl status airzone-backend"
echo "  sudo systemctl status airzone-frontend"
echo ""
echo "=========================================================================="
echo "Log Files"
echo "=========================================================================="
echo ""
echo "Backend logs:"
echo "  - Access: /var/log/airzone/backend-access.log"
echo "  - Error: /var/log/airzone/backend-error.log"
echo "  - Journal: journalctl -u airzone-backend"
echo ""
echo "Frontend logs:"
echo "  - Journal: journalctl -u airzone-frontend"
echo ""
echo "=========================================================================="
