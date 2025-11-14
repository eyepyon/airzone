#!/bin/bash
# ============================================================================
# Airzone Deployment Verification Script
# ============================================================================
#
# This script verifies that the Airzone deployment is configured correctly.
# It checks services, configurations, permissions, and connectivity.
#
# Usage: bash verify_deployment.sh
#
# ============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to print colored output
print_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

print_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

print_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# ============================================================================
# Check Functions
# ============================================================================

check_file_exists() {
    if [ -f "$1" ]; then
        print_pass "File exists: $1"
        return 0
    else
        print_fail "File missing: $1"
        return 1
    fi
}

check_dir_exists() {
    if [ -d "$1" ]; then
        print_pass "Directory exists: $1"
        return 0
    else
        print_fail "Directory missing: $1"
        return 1
    fi
}

check_service_active() {
    if systemctl is-active --quiet "$1"; then
        print_pass "Service active: $1"
        return 0
    else
        print_fail "Service not active: $1"
        return 1
    fi
}

check_service_enabled() {
    if systemctl is-enabled --quiet "$1"; then
        print_pass "Service enabled: $1"
        return 0
    else
        print_warn "Service not enabled: $1"
        return 1
    fi
}

check_port_listening() {
    if netstat -tuln 2>/dev/null | grep -q ":$1 " || ss -tuln 2>/dev/null | grep -q ":$1 "; then
        print_pass "Port listening: $1"
        return 0
    else
        print_fail "Port not listening: $1"
        return 1
    fi
}

check_command_exists() {
    if command -v "$1" &> /dev/null; then
        print_pass "Command available: $1"
        return 0
    else
        print_fail "Command not found: $1"
        return 1
    fi
}

# ============================================================================
# Start Verification
# ============================================================================

print_header "Airzone Deployment Verification"
print_info "Starting verification checks..."

# ============================================================================
# 1. System Commands
# ============================================================================

print_header "1. System Commands"

check_command_exists "apache2"
check_command_exists "python3"
check_command_exists "node"
check_command_exists "npm"
check_command_exists "mysql"
check_command_exists "systemctl"

# ============================================================================
# 2. Directory Structure
# ============================================================================

print_header "2. Directory Structure"

check_dir_exists "/var/www/airzone"
check_dir_exists "/var/www/airzone/backend"
check_dir_exists "/var/www/airzone/frontend"
check_dir_exists "/var/www/airzone/deployment"
check_dir_exists "/var/log/airzone"

# ============================================================================
# 3. Configuration Files
# ============================================================================

print_header "3. Configuration Files"

check_file_exists "/var/www/airzone/backend/.env"
check_file_exists "/var/www/airzone/frontend/.env.local"
check_file_exists "/etc/apache2/sites-available/airzone.conf"
check_file_exists "/etc/systemd/system/airzone-backend.service"
check_file_exists "/etc/systemd/system/airzone-frontend.service"

# ============================================================================
# 4. Backend Setup
# ============================================================================

print_header "4. Backend Setup"

check_dir_exists "/var/www/airzone/backend/venv"
check_file_exists "/var/www/airzone/backend/venv/bin/python"
check_file_exists "/var/www/airzone/backend/venv/bin/gunicorn"
check_file_exists "/var/www/airzone/backend/wsgi.py"
check_file_exists "/var/www/airzone/backend/app.py"

# ============================================================================
# 5. Frontend Setup
# ============================================================================

print_header "5. Frontend Setup"

check_dir_exists "/var/www/airzone/frontend/node_modules"
check_dir_exists "/var/www/airzone/frontend/.next"
check_file_exists "/var/www/airzone/frontend/.next/BUILD_ID"
check_file_exists "/var/www/airzone/frontend/package.json"

# ============================================================================
# 6. Apache Configuration
# ============================================================================

print_header "6. Apache Configuration"

# Check if Apache is running
if systemctl is-active --quiet apache2; then
    print_pass "Apache is running"
else
    print_fail "Apache is not running"
fi

# Check if site is enabled
if [ -L "/etc/apache2/sites-enabled/airzone.conf" ]; then
    print_pass "Airzone site is enabled"
else
    print_fail "Airzone site is not enabled"
fi

# Check Apache modules
for module in ssl rewrite headers proxy proxy_http wsgi; do
    if apache2ctl -M 2>/dev/null | grep -q "${module}_module"; then
        print_pass "Apache module enabled: $module"
    else
        print_fail "Apache module not enabled: $module"
    fi
done

# ============================================================================
# 7. Systemd Services
# ============================================================================

print_header "7. Systemd Services"

check_service_active "airzone-backend.service"
check_service_enabled "airzone-backend.service"
check_service_active "airzone-frontend.service"
check_service_enabled "airzone-frontend.service"

# ============================================================================
# 8. Network Ports
# ============================================================================

print_header "8. Network Ports"

check_port_listening "80"    # HTTP
check_port_listening "443"   # HTTPS
check_port_listening "3000"  # Next.js
check_port_listening "5000"  # Flask/Gunicorn

# ============================================================================
# 9. File Permissions
# ============================================================================

print_header "9. File Permissions"

# Check .env file permissions
if [ -f "/var/www/airzone/backend/.env" ]; then
    PERMS=$(stat -c "%a" /var/www/airzone/backend/.env 2>/dev/null || stat -f "%OLp" /var/www/airzone/backend/.env 2>/dev/null)
    if [ "$PERMS" = "600" ]; then
        print_pass "Backend .env permissions correct (600)"
    else
        print_warn "Backend .env permissions: $PERMS (should be 600)"
    fi
fi

if [ -f "/var/www/airzone/frontend/.env.local" ]; then
    PERMS=$(stat -c "%a" /var/www/airzone/frontend/.env.local 2>/dev/null || stat -f "%OLp" /var/www/airzone/frontend/.env.local 2>/dev/null)
    if [ "$PERMS" = "600" ]; then
        print_pass "Frontend .env.local permissions correct (600)"
    else
        print_warn "Frontend .env.local permissions: $PERMS (should be 600)"
    fi
fi

# Check ownership
if [ -d "/var/www/airzone" ]; then
    OWNER=$(stat -c "%U:%G" /var/www/airzone 2>/dev/null || stat -f "%Su:%Sg" /var/www/airzone 2>/dev/null)
    if [ "$OWNER" = "www-data:www-data" ]; then
        print_pass "Application directory ownership correct (www-data:www-data)"
    else
        print_warn "Application directory ownership: $OWNER (should be www-data:www-data)"
    fi
fi

# ============================================================================
# 10. SSL/TLS
# ============================================================================

print_header "10. SSL/TLS"

if [ -d "/etc/letsencrypt/live" ]; then
    CERT_DIRS=$(ls -1 /etc/letsencrypt/live 2>/dev/null | grep -v README)
    if [ -n "$CERT_DIRS" ]; then
        print_pass "SSL certificates found"
        for dir in $CERT_DIRS; do
            print_info "  Certificate: $dir"
        done
    else
        print_warn "No SSL certificates found"
    fi
else
    print_warn "Let's Encrypt directory not found"
fi

# ============================================================================
# 11. Connectivity Tests
# ============================================================================

print_header "11. Connectivity Tests"

# Test localhost connections
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null | grep -q "200\|404\|401"; then
    print_pass "Backend responds on localhost:5000"
else
    print_warn "Backend not responding on localhost:5000"
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null | grep -q "200\|404"; then
    print_pass "Frontend responds on localhost:3000"
else
    print_warn "Frontend not responding on localhost:3000"
fi

# ============================================================================
# 12. Log Files
# ============================================================================

print_header "12. Log Files"

check_file_exists "/var/log/apache2/airzone_error.log"
check_file_exists "/var/log/apache2/airzone_access.log"

if [ -d "/var/log/airzone" ]; then
    print_pass "Application log directory exists"
    if [ -f "/var/log/airzone/backend-error.log" ]; then
        print_pass "Backend error log exists"
    else
        print_info "Backend error log will be created on first run"
    fi
else
    print_fail "Application log directory missing"
fi

# ============================================================================
# Summary
# ============================================================================

print_header "Verification Summary"

echo ""
echo -e "${GREEN}Passed:${NC}   $PASSED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "${RED}Failed:${NC}   $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Deployment verification completed successfully!${NC}"
    echo ""
    print_info "Next steps:"
    echo "  1. Configure environment variables in .env files"
    echo "  2. Test the application: curl -I https://your-domain.com"
    echo "  3. Check logs: sudo journalctl -u airzone-backend -f"
    exit 0
else
    echo -e "${RED}✗ Deployment verification found issues${NC}"
    echo ""
    print_info "Please review the failed checks above and:"
    echo "  1. Fix any missing files or directories"
    echo "  2. Start any stopped services"
    echo "  3. Check configuration files"
    echo "  4. Review logs for errors"
    exit 1
fi
