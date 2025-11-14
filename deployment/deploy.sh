#!/bin/bash
# ============================================================================
# Airzone Complete Deployment Script
# ============================================================================
#
# This script automates the complete deployment of the Airzone platform.
# It should be run with sudo privileges on a fresh Ubuntu 20.04+ server.
#
# Usage: sudo bash deploy.sh
#
# Prerequisites:
# - Ubuntu 20.04 LTS or later
# - Domain name configured (airz.one)
# - MySQL 8.0+ installed
#
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="airz.one"
APP_DIR="/var/www/airzone"
LOG_DIR="/var/log/airzone"

# Function to print colored output
print_header() {
    echo ""
    echo -e "${MAGENTA}========================================================================${NC}"
    echo -e "${MAGENTA}$1${NC}"
    echo -e "${MAGENTA}========================================================================${NC}"
    echo ""
}

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

print_header "Airzone Deployment Script"
print_info "Starting deployment to $DOMAIN"
print_info "Application directory: $APP_DIR"
echo ""

# ============================================================================
# 1. System Update and Dependencies
# ============================================================================

print_header "Step 1: Installing System Dependencies"

print_step "Updating system packages..."
apt update
apt upgrade -y

print_step "Installing Apache and modules..."
apt install -y apache2 libapache2-mod-wsgi-py3

print_step "Installing Python..."
apt install -y python3.11 python3.11-venv python3-pip

print_step "Installing Node.js..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt install -y nodejs
else
    print_info "Node.js already installed"
fi

print_step "Installing certbot for SSL..."
apt install -y certbot python3-certbot-apache

print_step "Installing additional tools..."
apt install -y git curl wget ufw

print_info "System dependencies installed"

# ============================================================================
# 2. Create Directories and Set Permissions
# ============================================================================

print_header "Step 2: Setting Up Directories"

print_step "Creating application directories..."
mkdir -p $APP_DIR
mkdir -p $LOG_DIR
mkdir -p $APP_DIR/public

print_step "Setting ownership..."
chown -R www-data:www-data $APP_DIR
chown -R www-data:www-data $LOG_DIR

print_step "Setting permissions..."
chmod 755 $APP_DIR
chmod 755 $LOG_DIR

print_info "Directories created and configured"

# ============================================================================
# 3. Backend Setup
# ============================================================================

print_header "Step 3: Setting Up Backend"

cd $APP_DIR/backend

print_step "Creating Python virtual environment..."
sudo -u www-data python3.11 -m venv venv

print_step "Installing Python dependencies..."
sudo -u www-data bash -c "source venv/bin/activate && pip install --upgrade pip"
sudo -u www-data bash -c "source venv/bin/activate && pip install -r requirements.txt"
sudo -u www-data bash -c "source venv/bin/activate && pip install gunicorn"

print_step "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.production.example .env
    print_warning "Please edit $APP_DIR/backend/.env with production values"
    print_warning "Run: python3 $APP_DIR/scripts/generate_secrets.py"
else
    print_info "Backend .env already exists"
fi

chmod 600 .env
chown www-data:www-data .env

print_info "Backend setup complete"

# ============================================================================
# 4. Frontend Setup
# ============================================================================

print_header "Step 4: Setting Up Frontend"

cd $APP_DIR/frontend

print_step "Installing Node.js dependencies..."
sudo -u www-data npm install

print_step "Building frontend for production..."
sudo -u www-data npm run build

print_step "Setting up environment configuration..."
if [ ! -f ".env.local" ]; then
    cp .env.production.example .env.local
    print_warning "Please edit $APP_DIR/frontend/.env.local with production values"
else
    print_info "Frontend .env.local already exists"
fi

chmod 600 .env.local
chown www-data:www-data .env.local

print_info "Frontend setup complete"

# ============================================================================
# 5. Database Setup
# ============================================================================

print_header "Step 5: Database Setup"

print_warning "Database setup requires manual configuration"
print_info "Please run the following commands:"
echo ""
echo "  mysql -u root -p"
echo "  CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "  CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD';"
echo "  GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';"
echo "  FLUSH PRIVILEGES;"
echo "  EXIT;"
echo ""
echo "Then run database migrations:"
echo "  cd $APP_DIR/backend"
echo "  source venv/bin/activate"
echo "  python init_db.py"
echo ""

read -p "Press Enter when database setup is complete..."

# ============================================================================
# 6. Apache Configuration
# ============================================================================

print_header "Step 6: Configuring Apache"

cd $APP_DIR/deployment/apache

print_step "Running Apache setup script..."
bash setup_apache.sh

print_info "Apache configured"

# ============================================================================
# 7. Systemd Services
# ============================================================================

print_header "Step 7: Configuring Systemd Services"

cd $APP_DIR/deployment/systemd

print_step "Running systemd setup script..."
bash setup_services.sh

print_info "Systemd services configured"

# ============================================================================
# 8. SSL Certificate
# ============================================================================

print_header "Step 8: Obtaining SSL Certificate"

print_warning "SSL certificate setup requires domain to be pointing to this server"
print_info "Domain: $DOMAIN"
echo ""

read -p "Is your domain configured and pointing to this server? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Stopping Apache temporarily..."
    systemctl stop apache2
    
    print_step "Obtaining SSL certificate..."
    certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    
    print_step "Starting Apache..."
    systemctl start apache2
    
    print_info "SSL certificate obtained"
else
    print_warning "Skipping SSL certificate setup"
    print_info "Run manually later: sudo certbot --apache -d $DOMAIN -d www.$DOMAIN"
fi

# ============================================================================
# 9. Firewall Configuration
# ============================================================================

print_header "Step 9: Configuring Firewall"

print_step "Configuring UFW firewall..."

# Allow SSH (important!)
ufw allow OpenSSH

# Allow HTTP and HTTPS
ufw allow 'Apache Full'

# Enable firewall
print_warning "Enabling firewall. Make sure SSH is allowed!"
ufw --force enable

print_info "Firewall configured"

# ============================================================================
# 10. Final Checks
# ============================================================================

print_header "Step 10: Final Verification"

print_step "Checking service status..."

echo ""
print_info "Apache status:"
systemctl status apache2 --no-pager -l | head -n 5

echo ""
print_info "Backend service status:"
systemctl status airzone-backend --no-pager -l | head -n 5

echo ""
print_info "Frontend service status:"
systemctl status airzone-frontend --no-pager -l | head -n 5

# ============================================================================
# Deployment Complete
# ============================================================================

print_header "Deployment Complete!"

echo ""
print_info "✅ System dependencies installed"
print_info "✅ Application directories created"
print_info "✅ Backend configured"
print_info "✅ Frontend built"
print_info "✅ Apache configured"
print_info "✅ Systemd services running"
print_info "✅ Firewall enabled"
echo ""

print_warning "⚠️  Important Next Steps:"
echo ""
echo "1. Generate and configure secrets:"
echo "   cd $APP_DIR"
echo "   python3 scripts/generate_secrets.py"
echo "   # Copy output to backend/.env"
echo ""
echo "2. Configure environment variables:"
echo "   - Backend: $APP_DIR/backend/.env"
echo "   - Frontend: $APP_DIR/frontend/.env.local"
echo ""
echo "3. Configure external services:"
echo "   - Google OAuth (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)"
echo "   - Stripe (STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET)"
echo "   - Sui Blockchain (SUI_SPONSOR_PRIVATE_KEY, SUI_PACKAGE_ID)"
echo ""
echo "4. Restart services after configuration:"
echo "   sudo systemctl restart airzone-backend airzone-frontend"
echo ""
echo "5. Test the deployment:"
echo "   curl -I https://$DOMAIN"
echo "   curl https://$DOMAIN/api/v1/health"
echo ""

print_info "📚 Documentation:"
echo "   - Full guide: $APP_DIR/DEPLOYMENT_CONFIGURATION.md"
echo "   - Quick reference: $APP_DIR/deployment/QUICK_DEPLOY.md"
echo "   - Deployment files: $APP_DIR/deployment/"
echo ""

print_info "📊 Monitoring:"
echo "   - Backend logs: sudo journalctl -u airzone-backend -f"
echo "   - Frontend logs: sudo journalctl -u airzone-frontend -f"
echo "   - Apache logs: sudo tail -f /var/log/apache2/airzone_error.log"
echo ""

print_info "🔧 Useful Commands:"
echo "   - Restart: sudo systemctl restart airzone-backend airzone-frontend"
echo "   - Status: sudo systemctl status airzone-backend airzone-frontend"
echo "   - Logs: sudo journalctl -u airzone-backend -u airzone-frontend -f"
echo ""

print_header "Thank you for deploying Airzone!"
