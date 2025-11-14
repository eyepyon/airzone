# Airzone Deployment Files

This directory contains all the necessary configuration files and scripts for deploying the Airzone platform to a production server.

## Directory Structure

```
deployment/
├── apache/
│   ├── airzone.conf           # Apache virtual host configuration
│   └── setup_apache.sh        # Apache setup automation script
├── systemd/
│   ├── airzone-backend.service    # Backend systemd service
│   ├── airzone-frontend.service   # Frontend systemd service
│   └── setup_services.sh          # Service setup automation script
└── README.md                  # This file
```

## Quick Start

### 1. Prerequisites

Ensure your server meets the requirements:
- Ubuntu 20.04 LTS or later
- Apache 2.4+
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Minimum 2GB RAM, 20GB disk space

### 2. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Apache and modules
sudo apt install apache2 libapache2-mod-wsgi-py3 -y

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install MySQL
sudo apt install mysql-server -y

# Install certbot for SSL
sudo apt install certbot python3-certbot-apache -y
```

### 3. Clone and Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/airzone
cd /var/www/airzone

# Clone repository
git clone https://github.com/yourusername/airzone.git .

# Set ownership
sudo chown -R www-data:www-data /var/www/airzone
```

### 4. Configure Environment Variables

```bash
# Backend
cd /var/www/airzone/backend
cp .env.production.example .env

# Generate secrets
python3 ../scripts/generate_secrets.py

# Edit .env with generated secrets and production values
sudo nano .env
sudo chmod 600 .env
sudo chown www-data:www-data .env

# Frontend
cd /var/www/airzone/frontend
cp .env.production.example .env.local
sudo nano .env.local
sudo chmod 600 .env.local
sudo chown www-data:www-data .env.local
```

### 5. Setup Backend

```bash
cd /var/www/airzone/backend

# Create virtual environment
sudo -u www-data python3.11 -m venv venv

# Activate and install dependencies
sudo -u www-data bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Install Gunicorn
sudo -u www-data bash -c "source venv/bin/activate && pip install gunicorn"

# Setup database
sudo -u www-data bash -c "source venv/bin/activate && python init_db.py"
```

### 6. Setup Frontend

```bash
cd /var/www/airzone/frontend

# Install dependencies
sudo -u www-data npm install

# Build for production
sudo -u www-data npm run build
```

### 7. Setup Apache

```bash
cd /var/www/airzone/deployment/apache
sudo bash setup_apache.sh
```

### 8. Setup Systemd Services

```bash
cd /var/www/airzone/deployment/systemd
sudo bash setup_services.sh
```

### 9. Obtain SSL Certificate

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

### 10. Configure Firewall

```bash
# Allow HTTP and HTTPS
sudo ufw allow 'Apache Full'

# Allow SSH (if not already allowed)
sudo ufw allow OpenSSH

# Enable firewall
sudo ufw enable
```

## Apache Configuration

The Apache configuration (`apache/airzone.conf`) includes:

- **HTTP to HTTPS redirect**: All HTTP traffic is redirected to HTTPS
- **SSL/TLS configuration**: Modern TLS 1.3 with secure ciphers
- **Security headers**: HSTS, X-Frame-Options, CSP, etc.
- **Backend API**: Flask application served via mod_wsgi
- **Frontend**: Next.js application served via reverse proxy
- **Caching**: Static file caching with appropriate expiration
- **Compression**: Gzip compression for text-based content

### Key Features

1. **mod_wsgi for Flask**: Backend API runs as a WSGI application
2. **Reverse proxy for Next.js**: Frontend proxied from localhost:3000
3. **Security headers**: Comprehensive security headers including HSTS
4. **SSL/TLS**: Let's Encrypt certificates with automatic renewal
5. **Logging**: Separate access and error logs

### Setup Script

The `setup_apache.sh` script automates:
- Installing Apache and required modules
- Enabling necessary modules (ssl, rewrite, headers, proxy, wsgi)
- Copying configuration file
- Creating required directories
- Testing configuration
- Enabling site and reloading Apache

## Systemd Services

### Backend Service (`airzone-backend.service`)

Runs the Flask application using Gunicorn with:
- 4 worker processes
- 2 threads per worker
- Automatic restart on failure
- Logging to `/var/log/airzone/`
- Resource limits and security settings

### Frontend Service (`airzone-frontend.service`)

Runs the Next.js application with:
- Production mode
- Port 3000
- Automatic restart on failure
- Logging to systemd journal
- Security settings

### Setup Script

The `setup_services.sh` script automates:
- Creating log directory
- Installing Gunicorn (if needed)
- Building frontend (if needed)
- Installing service files
- Reloading systemd
- Enabling services
- Starting services
- Displaying status

## Service Management

### Start Services

```bash
sudo systemctl start airzone-backend
sudo systemctl start airzone-frontend
```

### Stop Services

```bash
sudo systemctl stop airzone-backend
sudo systemctl stop airzone-frontend
```

### Restart Services

```bash
sudo systemctl restart airzone-backend
sudo systemctl restart airzone-frontend
```

### Check Status

```bash
sudo systemctl status airzone-backend
sudo systemctl status airzone-frontend
```

### View Logs

```bash
# Backend logs
sudo journalctl -u airzone-backend -f
sudo tail -f /var/log/airzone/backend-error.log

# Frontend logs
sudo journalctl -u airzone-frontend -f
```

### Enable/Disable Auto-start

```bash
# Enable (start on boot)
sudo systemctl enable airzone-backend
sudo systemctl enable airzone-frontend

# Disable
sudo systemctl disable airzone-backend
sudo systemctl disable airzone-frontend
```

## Troubleshooting

### Apache Issues

```bash
# Test configuration
sudo apache2ctl configtest

# Check error logs
sudo tail -f /var/log/apache2/airzone_error.log

# Restart Apache
sudo systemctl restart apache2
```

### Backend Service Issues

```bash
# Check service status
sudo systemctl status airzone-backend

# View recent logs
sudo journalctl -u airzone-backend -n 50

# Check if Gunicorn is running
ps aux | grep gunicorn

# Test backend directly
cd /var/www/airzone/backend
source venv/bin/activate
python -c "from app import app; print(app)"
```

### Frontend Service Issues

```bash
# Check service status
sudo systemctl status airzone-frontend

# View recent logs
sudo journalctl -u airzone-frontend -n 50

# Check if Node.js is running
ps aux | grep node

# Test frontend directly
cd /var/www/airzone/frontend
npm start
```

### Database Connection Issues

```bash
# Check MySQL status
sudo systemctl status mysql

# Test database connection
mysql -u airzone_user -p airzone

# Check backend database configuration
cd /var/www/airzone/backend
source venv/bin/activate
python -c "from config import Config; print(Config.SQLALCHEMY_DATABASE_URI)"
```

### SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

## Security Checklist

- [ ] Strong, randomly generated secret keys
- [ ] Secure file permissions (600 for .env files)
- [ ] HTTPS enabled with valid SSL certificate
- [ ] HSTS headers configured
- [ ] Firewall enabled and configured
- [ ] Database user with limited privileges
- [ ] Regular security updates
- [ ] Log monitoring enabled
- [ ] Backup strategy in place

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

### Backup

```bash
# Database backup
mysqldump -u airzone_user -p airzone > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf airzone_backup_$(date +%Y%m%d).tar.gz /var/www/airzone
```

### Monitor Logs

```bash
# Watch all logs
sudo tail -f /var/log/apache2/airzone_error.log \
            /var/log/airzone/backend-error.log

# Or use journalctl
sudo journalctl -u airzone-backend -u airzone-frontend -f
```

## Support

For issues or questions:
1. Check the logs first
2. Review this documentation
3. Check the main DEPLOYMENT_CONFIGURATION.md
4. Contact system administrator

## Additional Resources

- [Apache Documentation](https://httpd.apache.org/docs/2.4/)
- [Systemd Documentation](https://www.freedesktop.org/software/systemd/man/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
