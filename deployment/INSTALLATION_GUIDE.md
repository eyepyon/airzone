# Airzone Installation Guide

Step-by-step installation guide for deploying Airzone to production.

## Prerequisites

Before starting, ensure you have:

- [ ] Ubuntu 20.04 LTS or later server
- [ ] Root or sudo access
- [ ] Domain name (airz.one) pointing to server IP
- [ ] MySQL 8.0+ installed
- [ ] At least 2GB RAM and 20GB disk space

## Installation Methods

Choose one of the following installation methods:

### Method 1: Automated Installation (Recommended)

**Time Required:** ~10 minutes

```bash
# 1. Clone repository
cd /var/www
sudo git clone <repository-url> airzone
cd airzone

# 2. Run automated deployment
sudo bash deployment/deploy.sh

# 3. Generate secrets
python3 scripts/generate_secrets.py

# 4. Edit configuration files
sudo nano backend/.env
sudo nano frontend/.env.local

# 5. Restart services
sudo systemctl restart airzone-backend airzone-frontend

# 6. Verify deployment
bash deployment/verify_deployment.sh
```

### Method 2: Manual Installation

**Time Required:** ~30 minutes

Follow the comprehensive guide: [DEPLOYMENT_CONFIGURATION.md](../DEPLOYMENT_CONFIGURATION.md)

### Method 3: Quick Installation (Experienced Admins)

**Time Required:** ~5 minutes

Follow the quick guide: [QUICK_DEPLOY.md](QUICK_DEPLOY.md)

## Step-by-Step Installation (Method 1 Detailed)

### Step 1: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
  apache2 \
  libapache2-mod-wsgi-py3 \
  python3.11 \
  python3.11-venv \
  python3-pip \
  nodejs \
  npm \
  mysql-server \
  certbot \
  python3-certbot-apache \
  git \
  curl \
  wget \
  ufw
```

### Step 2: Clone Repository

```bash
# Create application directory
sudo mkdir -p /var/www/airzone

# Clone repository
cd /var/www
sudo git clone <repository-url> airzone

# Set ownership
sudo chown -R www-data:www-data /var/www/airzone
```

### Step 3: Setup Database

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 4: Setup Backend

```bash
cd /var/www/airzone/backend

# Create virtual environment
sudo -u www-data python3.11 -m venv venv

# Install dependencies
sudo -u www-data bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Install Gunicorn
sudo -u www-data bash -c "source venv/bin/activate && pip install gunicorn"

# Copy environment template
sudo -u www-data cp .env.production.example .env

# Generate secrets
cd /var/www/airzone
python3 scripts/generate_secrets.py

# Edit .env with generated secrets
sudo nano backend/.env

# Set permissions
sudo chmod 600 backend/.env
sudo chown www-data:www-data backend/.env

# Initialize database
cd backend
sudo -u www-data bash -c "source venv/bin/activate && python init_db.py"
```

### Step 5: Setup Frontend

```bash
cd /var/www/airzone/frontend

# Install dependencies
sudo -u www-data npm install

# Build for production
sudo -u www-data npm run build

# Copy environment template
sudo -u www-data cp .env.production.example .env.local

# Edit .env.local
sudo nano .env.local

# Set permissions
sudo chmod 600 .env.local
sudo chown www-data:www-data .env.local
```

### Step 6: Configure Apache

```bash
cd /var/www/airzone/deployment/apache

# Run Apache setup script
sudo bash setup_apache.sh

# Or manually:
# sudo cp airzone.conf /etc/apache2/sites-available/
# sudo a2enmod ssl rewrite headers proxy proxy_http wsgi
# sudo a2ensite airzone.conf
# sudo a2dissite 000-default.conf
# sudo apache2ctl configtest
# sudo systemctl reload apache2
```

### Step 7: Configure Systemd Services

```bash
cd /var/www/airzone/deployment/systemd

# Run systemd setup script
sudo bash setup_services.sh

# Or manually:
# sudo cp airzone-backend.service /etc/systemd/system/
# sudo cp airzone-frontend.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl enable airzone-backend airzone-frontend
# sudo systemctl start airzone-backend airzone-frontend
```

### Step 8: Obtain SSL Certificate

```bash
# Stop Apache temporarily
sudo systemctl stop apache2

# Obtain certificate
sudo certbot certonly --standalone -d airz.one -d www.airz.one

# Start Apache
sudo systemctl start apache2

# Test auto-renewal
sudo certbot renew --dry-run
```

### Step 9: Configure Firewall

```bash
# Allow SSH (important!)
sudo ufw allow OpenSSH

# Allow HTTP and HTTPS
sudo ufw allow 'Apache Full'

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Step 10: Verify Installation

```bash
# Run verification script
cd /var/www/airzone
bash deployment/verify_deployment.sh

# Check services
sudo systemctl status apache2 airzone-backend airzone-frontend

# Test endpoints
curl -I https://airz.one
curl https://airz.one/api/v1/health

# Check logs
sudo journalctl -u airzone-backend -n 20
sudo journalctl -u airzone-frontend -n 20
```

## Configuration

### Backend Environment Variables

Edit `/var/www/airzone/backend/.env`:

```bash
# Required Configuration
SECRET_KEY=<generated-secret-key>
JWT_SECRET_KEY=<generated-jwt-secret>
ENCRYPTION_KEY=<generated-encryption-key>

# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airzone
DB_USER=airzone_user
DB_PASSWORD=<your-database-password>

# Google OAuth
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>

# Stripe
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>
STRIPE_WEBHOOK_SECRET=<your-stripe-webhook-secret>

# Sui Blockchain
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=<your-sponsor-private-key>
SUI_PACKAGE_ID=<your-deployed-package-id>

# CORS
CORS_ORIGINS=https://airz.one,https://www.airz.one
```

### Frontend Environment Variables

Edit `/var/www/airzone/frontend/.env.local`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://airz.one/api/v1

# Sui Blockchain
NEXT_PUBLIC_SUI_NETWORK=testnet
NEXT_PUBLIC_SUI_RPC_URL=https://fullnode.testnet.sui.io:443

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>

# Google OAuth
NEXT_PUBLIC_GOOGLE_CLIENT_ID=<your-google-client-id>

# Application
NEXT_PUBLIC_APP_URL=https://airz.one
NEXT_PUBLIC_APP_NAME=Airzone
```

## Post-Installation

### 1. Configure External Services

#### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URIs
4. Copy Client ID and Secret to `.env`

#### Stripe
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Get API keys from Developers > API keys
3. Set up webhook endpoint: `https://airz.one/api/v1/payments/webhook`
4. Copy keys to `.env`

#### Sui Blockchain
1. Generate sponsor wallet: `python3 scripts/generate_sponsor_wallet.py`
2. Deploy smart contract: `bash scripts/deploy_contract.sh`
3. Copy package ID to `.env`

### 2. Test Complete Flow

```bash
# 1. Test authentication
curl -X POST https://airz.one/api/v1/auth/google \
  -H "Content-Type: application/json" \
  -d '{"id_token": "test-token"}'

# 2. Test NFT endpoints
curl https://airz.one/api/v1/nfts

# 3. Test product endpoints
curl https://airz.one/api/v1/products

# 4. Test frontend
curl -I https://airz.one
```

### 3. Set Up Monitoring

```bash
# View logs in real-time
sudo journalctl -u airzone-backend -u airzone-frontend -f

# Set up log rotation (optional)
sudo nano /etc/logrotate.d/airzone
```

### 4. Configure Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup-airzone.sh

# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-airzone.sh
```

## Troubleshooting

### Backend Issues

```bash
# Check service status
sudo systemctl status airzone-backend

# View logs
sudo journalctl -u airzone-backend -n 50

# Test Python environment
cd /var/www/airzone/backend
source venv/bin/activate
python -c "from app import app; print(app)"
```

### Frontend Issues

```bash
# Check service status
sudo systemctl status airzone-frontend

# View logs
sudo journalctl -u airzone-frontend -n 50

# Rebuild frontend
cd /var/www/airzone/frontend
sudo -u www-data npm run build
```

### Apache Issues

```bash
# Test configuration
sudo apache2ctl configtest

# Check error logs
sudo tail -f /var/log/apache2/airzone_error.log

# Restart Apache
sudo systemctl restart apache2
```

### Database Issues

```bash
# Test connection
mysql -u airzone_user -p airzone

# Check tables
mysql -u airzone_user -p -e "USE airzone; SHOW TABLES;"

# Run migrations
cd /var/www/airzone/backend
source venv/bin/activate
alembic upgrade head
```

## Maintenance

### Update Application

```bash
# Pull latest code
cd /var/www/airzone
sudo -u www-data git pull

# Update backend
cd backend
sudo -u www-data bash -c "source venv/bin/activate && pip install -r requirements.txt"
sudo -u www-data bash -c "source venv/bin/activate && alembic upgrade head"
sudo systemctl restart airzone-backend

# Update frontend
cd ../frontend
sudo -u www-data npm install
sudo -u www-data npm run build
sudo systemctl restart airzone-frontend
```

### Backup Database

```bash
# Create backup
mysqldump -u airzone_user -p airzone > backup_$(date +%Y%m%d).sql

# Restore backup
mysql -u airzone_user -p airzone < backup_20240101.sql
```

## Support

For help with installation:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [DEPLOYMENT_CONFIGURATION.md](../DEPLOYMENT_CONFIGURATION.md)
3. Run verification: `bash deployment/verify_deployment.sh`
4. Check logs for error messages
5. Contact system administrator

## Additional Resources

- [Deployment Configuration](../DEPLOYMENT_CONFIGURATION.md) - Comprehensive guide
- [Quick Deploy](QUICK_DEPLOY.md) - Fast deployment for experienced admins
- [Deployment Checklist](../DEPLOYMENT_CHECKLIST.md) - Verification checklist
- [Deployment Index](../DEPLOYMENT_INDEX.md) - Documentation index

---

**Installation Complete!** 🎉

Your Airzone platform should now be running at https://airz.one
