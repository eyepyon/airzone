#!/bin/bash
# ============================================================================
# Apache Setup Script for Airzone
# ============================================================================
#
# This script automates the Apache web server setup for the Airzone platform.
# It should be run with sudo privileges.
#
# Usage: sudo bash setup_apache.sh
#
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run as root (use sudo)"
    exit 1
fi

print_info "Starting Apache setup for Airzone..."

# ============================================================================
# 1. Install Apache and Required Modules
# ============================================================================

print_info "Installing Apache and required modules..."

apt update
apt install -y apache2 libapache2-mod-wsgi-py3

# ============================================================================
# 2. Enable Required Apache Modules
# ============================================================================

print_info "Enabling Apache modules..."

a2enmod ssl
a2enmod rewrite
a2enmod headers
a2enmod proxy
a2enmod proxy_http
a2enmod wsgi
a2enmod expires
a2enmod deflate

# ============================================================================
# 3. Copy Apache Configuration
# ============================================================================

print_info "Installing Apache configuration..."

# Check if configuration file exists
if [ ! -f "airzone.conf" ]; then
    print_error "airzone.conf not found in current directory"
    print_info "Please run this script from the deployment/apache directory"
    exit 1
fi

# Backup existing configuration if it exists
if [ -f "/etc/apache2/sites-available/airzone.conf" ]; then
    print_warning "Backing up existing configuration..."
    cp /etc/apache2/sites-available/airzone.conf \
       /etc/apache2/sites-available/airzone.conf.backup.$(date +%Y%m%d_%H%M%S)
fi

# Copy new configuration
cp airzone.conf /etc/apache2/sites-available/airzone.conf

print_info "Apache configuration installed"

# ============================================================================
# 4. Create Required Directories
# ============================================================================

print_info "Creating required directories..."

mkdir -p /var/www/airzone/public
mkdir -p /var/log/airzone

# Set ownership
chown -R www-data:www-data /var/www/airzone
chown -R www-data:www-data /var/log/airzone

# Set permissions
chmod 755 /var/www/airzone
chmod 755 /var/log/airzone

print_info "Directories created"

# ============================================================================
# 5. Test Apache Configuration
# ============================================================================

print_info "Testing Apache configuration..."

if apache2ctl configtest; then
    print_info "Apache configuration test passed"
else
    print_error "Apache configuration test failed"
    print_info "Please check the configuration and try again"
    exit 1
fi

# ============================================================================
# 6. Enable Site
# ============================================================================

print_info "Enabling Airzone site..."

# Disable default site
a2dissite 000-default.conf 2>/dev/null || true

# Enable Airzone site
a2ensite airzone.conf

print_info "Site enabled"

# ============================================================================
# 7. Reload Apache
# ============================================================================

print_info "Reloading Apache..."

systemctl reload apache2

if systemctl is-active --quiet apache2; then
    print_info "Apache is running"
else
    print_warning "Apache is not running. Starting..."
    systemctl start apache2
fi

# ============================================================================
# 8. Display Status
# ============================================================================

echo ""
print_info "Apache setup completed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Obtain SSL certificate: sudo certbot --apache -d airz.one -d www.airz.one"
echo "  2. Set up systemd services for backend and frontend"
echo "  3. Configure firewall: sudo ufw allow 'Apache Full'"
echo "  4. Test the configuration: curl -I http://localhost"
echo ""
print_info "Apache status:"
systemctl status apache2 --no-pager -l

echo ""
print_info "Enabled sites:"
apache2ctl -S

echo ""
print_info "Log files:"
echo "  - Error log: /var/log/apache2/airzone_error.log"
echo "  - Access log: /var/log/apache2/airzone_access.log"
echo "  - WSGI log: /var/log/airzone/wsgi.log"
