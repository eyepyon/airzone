# Airzone Deployment Checklist

Use this checklist to ensure all deployment steps are completed correctly.

## Pre-Deployment

### Server Setup
- [ ] Ubuntu 20.04+ server provisioned
- [ ] Root/sudo access configured
- [ ] Domain name registered (airz.one)
- [ ] DNS A records pointing to server IP
- [ ] SSH access configured
- [ ] Firewall rules planned

### External Services
- [ ] Google Cloud Console project created
- [ ] Google OAuth credentials obtained
- [ ] Stripe account created
- [ ] Stripe API keys obtained (test and live)
- [ ] Sui wallet for sponsoring created
- [ ] Sui smart contract deployed

## System Installation

### Dependencies
- [ ] System packages updated (`apt update && apt upgrade`)
- [ ] Apache 2.4+ installed
- [ ] mod_wsgi installed
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] MySQL 8.0+ installed
- [ ] Certbot installed
- [ ] Git installed

### Application Files
- [ ] Repository cloned to `/var/www/airzone`
- [ ] File ownership set to `www-data:www-data`
- [ ] Directory permissions set correctly (755 for dirs, 644 for files)

## Configuration

### Backend Configuration
- [ ] `.env` file created from `.env.production.example`
- [ ] `SECRET_KEY` generated (64+ characters)
- [ ] `JWT_SECRET_KEY` generated (64+ characters)
- [ ] `ENCRYPTION_KEY` generated (64 hex characters)
- [ ] Database credentials configured
- [ ] Google OAuth credentials added
- [ ] Stripe API keys added (live keys for production)
- [ ] Sui network configured (testnet or mainnet)
- [ ] Sui sponsor private key added
- [ ] Sui package ID added
- [ ] CORS origins configured
- [ ] `.env` file permissions set to 600
- [ ] `.env` file owned by www-data

### Frontend Configuration
- [ ] `.env.local` file created from `.env.production.example`
- [ ] `NEXT_PUBLIC_API_URL` set to production URL
- [ ] `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` added (live key)
- [ ] `NEXT_PUBLIC_GOOGLE_CLIENT_ID` added
- [ ] `NEXT_PUBLIC_SUI_NETWORK` configured
- [ ] `.env.local` file permissions set to 600
- [ ] `.env.local` file owned by www-data

### Database Setup
- [ ] MySQL database created (`airzone`)
- [ ] Database user created (`airzone_user`)
- [ ] User privileges granted
- [ ] Database connection tested
- [ ] Alembic migrations run (`alembic upgrade head`)
- [ ] Initial data seeded (if applicable)

## Backend Setup

### Python Environment
- [ ] Virtual environment created (`python3.11 -m venv venv`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Gunicorn installed (`pip install gunicorn`)
- [ ] Application imports tested (`python -c "from app import app"`)

### WSGI Configuration
- [ ] `wsgi.py` file exists in backend directory
- [ ] WSGI file permissions correct (644)
- [ ] WSGI log directory created (`/var/log/airzone`)

## Frontend Setup

### Node.js Environment
- [ ] Node modules installed (`npm install`)
- [ ] Production build created (`npm run build`)
- [ ] Build successful (`.next/BUILD_ID` exists)
- [ ] Build artifacts owned by www-data

## Apache Configuration

### Apache Setup
- [ ] Apache configuration file copied to `/etc/apache2/sites-available/`
- [ ] Required modules enabled (ssl, rewrite, headers, proxy, wsgi)
- [ ] Configuration tested (`apache2ctl configtest`)
- [ ] Default site disabled
- [ ] Airzone site enabled
- [ ] Apache reloaded

### SSL/TLS
- [ ] SSL certificate obtained (Let's Encrypt)
- [ ] Certificate files exist in `/etc/letsencrypt/live/`
- [ ] Apache SSL configuration updated
- [ ] HTTPS redirect working
- [ ] Certificate auto-renewal configured
- [ ] Auto-renewal tested (`certbot renew --dry-run`)

### Security Headers
- [ ] HSTS header configured
- [ ] X-Frame-Options header set
- [ ] X-Content-Type-Options header set
- [ ] X-XSS-Protection header set
- [ ] Referrer-Policy header set
- [ ] Content-Security-Policy configured

## Systemd Services

### Backend Service
- [ ] Service file copied to `/etc/systemd/system/`
- [ ] Service file permissions set (644)
- [ ] Systemd daemon reloaded
- [ ] Service enabled (`systemctl enable airzone-backend`)
- [ ] Service started (`systemctl start airzone-backend`)
- [ ] Service status checked (active/running)
- [ ] Service logs reviewed (no errors)

### Frontend Service
- [ ] Service file copied to `/etc/systemd/system/`
- [ ] Service file permissions set (644)
- [ ] Systemd daemon reloaded
- [ ] Service enabled (`systemctl enable airzone-frontend`)
- [ ] Service started (`systemctl start airzone-frontend`)
- [ ] Service status checked (active/running)
- [ ] Service logs reviewed (no errors)

## Firewall Configuration

### UFW Setup
- [ ] UFW installed
- [ ] SSH allowed (`ufw allow OpenSSH`)
- [ ] HTTP/HTTPS allowed (`ufw allow 'Apache Full'`)
- [ ] UFW enabled
- [ ] Rules verified (`ufw status`)

## Testing

### Basic Connectivity
- [ ] HTTP redirects to HTTPS
- [ ] HTTPS loads without certificate errors
- [ ] Homepage loads correctly
- [ ] API health endpoint responds (`/api/v1/health`)

### Backend API
- [ ] Auth endpoints accessible
- [ ] NFT endpoints accessible
- [ ] Product endpoints accessible
- [ ] Order endpoints accessible
- [ ] Payment endpoints accessible
- [ ] WiFi endpoints accessible
- [ ] Error responses formatted correctly

### Frontend
- [ ] All pages load correctly
- [ ] Static assets load (images, CSS, JS)
- [ ] Client-side routing works
- [ ] API calls succeed
- [ ] Authentication flow works

### Integration
- [ ] Google OAuth login works
- [ ] Wallet creation works
- [ ] NFT minting works
- [ ] Product listing works
- [ ] Order creation works
- [ ] Stripe payment works
- [ ] WiFi captive portal works

## Security Verification

### File Permissions
- [ ] `.env` files are 600
- [ ] Application files owned by www-data
- [ ] No world-writable files
- [ ] Log files have appropriate permissions

### Network Security
- [ ] Only necessary ports open (22, 80, 443)
- [ ] SSH key authentication configured
- [ ] Password authentication disabled (optional)
- [ ] Fail2ban configured (optional)

### Application Security
- [ ] Debug mode disabled in production
- [ ] Strong secret keys in use
- [ ] Database credentials secure
- [ ] API keys not exposed in frontend
- [ ] CORS properly configured
- [ ] Rate limiting enabled

## Monitoring and Logging

### Log Files
- [ ] Apache logs accessible
- [ ] Backend logs accessible
- [ ] Frontend logs accessible
- [ ] Log rotation configured
- [ ] Disk space monitored

### Service Monitoring
- [ ] Services set to restart on failure
- [ ] Service status can be checked
- [ ] Logs can be viewed with journalctl

## Backup and Recovery

### Backup Strategy
- [ ] Database backup script created
- [ ] Application backup script created
- [ ] Backup schedule configured
- [ ] Backup storage location configured
- [ ] Backup restoration tested

## Documentation

### Deployment Docs
- [ ] Deployment guide reviewed
- [ ] Configuration documented
- [ ] Credentials stored securely
- [ ] Runbook created for common tasks
- [ ] Contact information documented

## Post-Deployment

### Final Checks
- [ ] All services running
- [ ] No errors in logs
- [ ] Performance acceptable
- [ ] SSL certificate valid
- [ ] Monitoring in place

### Handoff
- [ ] Deployment documented
- [ ] Credentials shared securely
- [ ] Support contacts provided
- [ ] Maintenance schedule established

## Maintenance Tasks

### Regular Tasks
- [ ] Monitor logs daily
- [ ] Check service status daily
- [ ] Review security updates weekly
- [ ] Update dependencies monthly
- [ ] Rotate logs monthly
- [ ] Test backups monthly
- [ ] Review SSL certificate expiry
- [ ] Update application as needed

## Rollback Plan

### If Deployment Fails
- [ ] Backup of previous version available
- [ ] Rollback procedure documented
- [ ] Database rollback plan ready
- [ ] DNS rollback plan ready (if applicable)

## Sign-Off

- [ ] Deployment completed by: _________________ Date: _________
- [ ] Deployment verified by: _________________ Date: _________
- [ ] Production approved by: _________________ Date: _________

## Notes

Use this section for deployment-specific notes, issues encountered, or deviations from the standard process:

```
[Add notes here]
```

---

**Deployment Status:** ⬜ Not Started | ⬜ In Progress | ⬜ Complete | ⬜ Failed

**Deployment Date:** __________________

**Deployed By:** __________________

**Version:** __________________
