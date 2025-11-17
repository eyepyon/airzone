# Airzone Deployment Configuration Guide

This guide covers the deployment configuration for the Airzone platform on a production server.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Secret Key Generation](#secret-key-generation)
4. [Apache Web Server Setup](#apache-web-server-setup)
5. [Systemd Services](#systemd-services)
6. [SSL/TLS Configuration](#ssltls-configuration)
7. [Security Checklist](#security-checklist)

## Prerequisites

### System Requirements

- Ubuntu 20.04 LTS or later (or equivalent Linux distribution)
- Apache 2.4+
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Minimum 2GB RAM, 20GB disk space

### Required Software

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Apache and modules
sudo apt install apache2 libapache2-mod-wsgi-py3 -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js (via NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install MySQL
sudo apt install mysql-server -y

# Install certbot for SSL
sudo apt install certbot python3-certbot-apache -y
```

## Environment Configuration

### 1. Backend Configuration

```bash
cd /var/www/airzone/backend

# Copy production environment template
cp .env.production.example .env

# Generate secure secret keys
python3 ../scripts/generate_secrets.py

# Edit .env file with generated keys and production values
nano .env
```

**Required Configuration:**

- `SECRET_KEY`: Flask secret key (64+ characters)
- `JWT_SECRET_KEY`: JWT signing key (64+ characters)
- `ENCRYPTION_KEY`: Wallet encryption key (64 hex characters)
- `DB_PASSWORD`: Strong database password
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: From Google Cloud Console
- `STRIPE_SECRET_KEY` & `STRIPE_WEBHOOK_SECRET`: From Stripe Dashboard
- `XRPL_SPONSOR_SEED`: Generated sponsor wallet seed

**Set secure file permissions:**

```bash
chmod 600 .env
chown www-data:www-data .env
```

### 2. Frontend Configuration

```bash
cd /var/www/airzone/frontend

# Copy production environment template
cp .env.production.example .env.local

# Edit with production values
nano .env.local
```

**Required Configuration:**

- `NEXT_PUBLIC_API_URL`: Backend API URL (https://airz.one/api/v1)
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `NEXT_PUBLIC_GOOGLE_CLIENT_ID`: Google OAuth client ID
- `NEXT_PUBLIC_XRPL_NETWORK`: testnet or mainnet

## Secret Key Generation

### Generate All Secrets at Once

```bash
cd /var/www/airzone
python3 scripts/generate_secrets.py
```

This generates:
- Flask SECRET_KEY
- JWT_SECRET_KEY
- ENCRYPTION_KEY

**⚠️ IMPORTANT:**
- Store these keys securely
- Never commit to version control
- Keep backups in a secure location
- Rotate keys periodically

### Generate Sui Sponsor Wallet

```bash
cd /var/www/airzone
python3 scripts/generate_sponsor_wallet.py
```

This creates a new Sui wallet for sponsoring NFT minting transactions.

## Apache Web Server Setup

### 1. Create Apache Configuration

Create `/etc/apache2/sites-available/airzone.conf`:

```apache
<VirtualHost *:80>
    ServerName airz.one
    ServerAlias www.airz.one
    
    # Redirect HTTP to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
</VirtualHost>

<VirtualHost *:443>
    ServerName airz.one
    ServerAlias www.airz.one
    
    # SSL Configuration (managed by certbot)
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/airz.one/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/airz.one/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Backend API (Flask with mod_wsgi)
    WSGIDaemonProcess airzone_backend python-home=/var/www/airzone/backend/venv python-path=/var/www/airzone/backend
    WSGIProcessGroup airzone_backend
    WSGIScriptAlias /api /var/www/airzone/backend/wsgi.py
    
    <Directory /var/www/airzone/backend>
        Require all granted
    </Directory>
    
    # Frontend (Next.js via reverse proxy)
    ProxyPreserveHost On
    ProxyPass /api !
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/
    
    # Logging
    ErrorLog ${APACHE_LOG_DIR}/airzone_error.log
    CustomLog ${APACHE_LOG_DIR}/airzone_access.log combined
</VirtualHost>
```

### 2. Enable Apache Modules

```bash
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod wsgi
```

### 3. Enable Site Configuration

```bash
sudo a2ensite airzone.conf
sudo a2dissite 000-default.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

## Systemd Services

### 1. Backend Service

Create `/etc/systemd/system/airzone-backend.service`:

```ini
[Unit]
Description=Airzone Backend Flask Application
After=network.target mysql.service
Requires=mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/airzone/backend
Environment="PATH=/var/www/airzone/backend/venv/bin"
ExecStart=/var/www/airzone/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/airzone/backend-access.log \
    --error-logfile /var/log/airzone/backend-error.log \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Frontend Service

Create `/etc/systemd/system/airzone-frontend.service`:

```ini
[Unit]
Description=Airzone Frontend Next.js Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/airzone/frontend
Environment="NODE_ENV=production"
Environment="PORT=3000"
ExecStart=/usr/bin/npm start

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Services

```bash
# Create log directory
sudo mkdir -p /var/log/airzone
sudo chown www-data:www-data /var/log/airzone

# Reload systemd
sudo systemctl daemon-reload

# Enable services (start on boot)
sudo systemctl enable airzone-backend
sudo systemctl enable airzone-frontend

# Start services
sudo systemctl start airzone-backend
sudo systemctl start airzone-frontend

# Check status
sudo systemctl status airzone-backend
sudo systemctl status airzone-frontend
```

## SSL/TLS Configuration

### 1. Obtain SSL Certificate with Let's Encrypt

```bash
# Stop Apache temporarily
sudo systemctl stop apache2

# Obtain certificate
sudo certbot certonly --standalone -d airz.one -d www.airz.one

# Start Apache
sudo systemctl start apache2
```

### 2. Auto-Renewal

Certbot automatically sets up renewal. Test it:

```bash
sudo certbot renew --dry-run
```

### 3. Configure HSTS

HSTS headers are already included in the Apache configuration above.

## Security Checklist

### File Permissions

```bash
# Backend
sudo chown -R www-data:www-data /var/www/airzone/backend
sudo chmod 600 /var/www/airzone/backend/.env
sudo chmod 755 /var/www/airzone/backend

# Frontend
sudo chown -R www-data:www-data /var/www/airzone/frontend
sudo chmod 600 /var/www/airzone/frontend/.env.local
sudo chmod 755 /var/www/airzone/frontend
```

### Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 'Apache Full'

# Allow SSH (if not already allowed)
sudo ufw allow OpenSSH

# Enable firewall
sudo ufw enable
```

### Database Security

```bash
# Run MySQL secure installation
sudo mysql_secure_installation

# Create dedicated database user
mysql -u root -p
```

```sql
CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Security Best Practices

- ✅ Use strong, randomly generated passwords
- ✅ Enable HTTPS with valid SSL certificate
- ✅ Set HSTS headers
- ✅ Restrict file permissions (600 for .env files)
- ✅ Enable firewall (ufw)
- ✅ Keep system and packages updated
- ✅ Use environment variables for secrets
- ✅ Enable rate limiting
- ✅ Regular security audits
- ✅ Monitor logs for suspicious activity

## Verification

### 1. Check Services

```bash
# Backend
curl http://localhost:5000/api/v1/health

# Frontend
curl http://localhost:3000

# Apache
sudo systemctl status apache2

# Services
sudo systemctl status airzone-backend
sudo systemctl status airzone-frontend
```

### 2. Check Logs

```bash
# Apache logs
sudo tail -f /var/log/apache2/airzone_error.log

# Backend logs
sudo tail -f /var/log/airzone/backend-error.log

# Frontend logs
sudo journalctl -u airzone-frontend -f

# System logs
sudo journalctl -xe
```

### 3. Test HTTPS

```bash
# Test SSL configuration
curl -I https://airz.one

# Check SSL certificate
openssl s_client -connect airz.one:443 -servername airz.one
```

## Troubleshooting

### Backend Not Starting

```bash
# Check logs
sudo journalctl -u airzone-backend -n 50

# Check Python environment
cd /var/www/airzone/backend
source venv/bin/activate
python -c "import app"

# Check database connection
python -c "from app import db; db.create_all()"
```

### Frontend Not Starting

```bash
# Check logs
sudo journalctl -u airzone-frontend -n 50

# Check Node.js
cd /var/www/airzone/frontend
npm run build
```

### Apache Issues

```bash
# Test configuration
sudo apache2ctl configtest

# Check error logs
sudo tail -f /var/log/apache2/error.log

# Restart Apache
sudo systemctl restart apache2
```

## Maintenance

### Update Application

```bash
# Backend
cd /var/www/airzone/backend
git pull
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart airzone-backend

# Frontend
cd /var/www/airzone/frontend
git pull
npm install
npm run build
sudo systemctl restart airzone-frontend
```

### Backup

```bash
# Database backup
mysqldump -u airzone_user -p airzone > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf airzone_backup_$(date +%Y%m%d).tar.gz /var/www/airzone
```

## Support

For issues or questions:
- Check logs first
- Review this documentation
- Contact system administrator
