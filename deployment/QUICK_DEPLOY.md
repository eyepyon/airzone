# Airzone Quick Deployment Guide

This is a condensed deployment guide for experienced system administrators. For detailed instructions, see `DEPLOYMENT_CONFIGURATION.md`.

## Prerequisites

- Ubuntu 20.04+ server with root access
- Domain name pointing to server IP (airz.one)
- MySQL 8.0+ installed and running

## One-Command Setup (After Prerequisites)

```bash
# Clone repository
cd /var/www && sudo git clone https://github.com/yourusername/airzone.git
cd airzone

# Run automated deployment
sudo bash deployment/deploy.sh
```

## Manual Step-by-Step (5 Minutes)

### 1. System Setup (1 min)

```bash
sudo apt update && sudo apt install -y apache2 libapache2-mod-wsgi-py3 \
  python3.11 python3.11-venv nodejs npm mysql-server certbot python3-certbot-apache
```

### 2. Application Setup (2 min)

```bash
cd /var/www/airzone

# Backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn
cp .env.production.example .env
# Edit .env with production values
python init_db.py
deactivate

# Frontend
cd ../frontend
npm install
npm run build
cp .env.production.example .env.local
# Edit .env.local with production values

# Set ownership
sudo chown -R www-data:www-data /var/www/airzone
```

### 3. Generate Secrets (30 sec)

```bash
cd /var/www/airzone
python3 scripts/generate_secrets.py
# Copy output to backend/.env
```

### 4. Apache Setup (30 sec)

```bash
cd deployment/apache
sudo bash setup_apache.sh
```

### 5. Systemd Services (30 sec)

```bash
cd ../systemd
sudo bash setup_services.sh
```

### 6. SSL Certificate (30 sec)

```bash
sudo systemctl stop apache2
sudo certbot certonly --standalone -d airz.one -d www.airz.one
sudo systemctl start apache2
```

### 7. Firewall (30 sec)

```bash
sudo ufw allow 'Apache Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Verification

```bash
# Check services
sudo systemctl status airzone-backend airzone-frontend apache2

# Test endpoints
curl -I https://airz.one
curl https://airz.one/api/v1/health

# Check logs
sudo journalctl -u airzone-backend -n 20
sudo journalctl -u airzone-frontend -n 20
```

## Essential Commands

```bash
# Restart services
sudo systemctl restart airzone-backend airzone-frontend

# View logs
sudo journalctl -u airzone-backend -f
sudo tail -f /var/log/airzone/backend-error.log

# Update application
cd /var/www/airzone && git pull
sudo systemctl restart airzone-backend airzone-frontend
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check `/var/log/airzone/backend-error.log` |
| Frontend won't start | Run `npm run build` in frontend directory |
| Apache config error | Run `sudo apache2ctl configtest` |
| SSL certificate error | Run `sudo certbot renew` |
| Database connection error | Check `.env` DB credentials |

## Security Checklist

- [ ] Generated strong secrets with `generate_secrets.py`
- [ ] Set `.env` file permissions to 600
- [ ] Enabled HTTPS with Let's Encrypt
- [ ] Configured firewall with ufw
- [ ] Created dedicated MySQL user
- [ ] Set proper file ownership (www-data)

## Next Steps

1. Configure Google OAuth credentials
2. Configure Stripe API keys
3. Deploy Sui smart contract
4. Generate sponsor wallet
5. Test complete user flow
6. Set up monitoring and backups

## Support

- Full documentation: `DEPLOYMENT_CONFIGURATION.md`
- Deployment files: `deployment/` directory
- Issues: Check logs first, then contact admin
