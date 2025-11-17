# Airzone Deployment Documentation Index

Quick reference guide to all deployment-related documentation and files.

## 📚 Documentation

### Main Guides

| Document | Purpose | Audience |
|----------|---------|----------|
| [DEPLOYMENT_CONFIGURATION.md](DEPLOYMENT_CONFIGURATION.md) | Comprehensive deployment guide with detailed instructions | System administrators, DevOps |
| [deployment/QUICK_DEPLOY.md](deployment/QUICK_DEPLOY.md) | Condensed 5-minute deployment guide | Experienced administrators |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Step-by-step verification checklist | All deployers |
| [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) | Overview of what was implemented | Project managers, developers |
| [deployment/README.md](deployment/README.md) | Deployment files documentation | All deployers |

### Quick Links

- **Getting Started:** [DEPLOYMENT_CONFIGURATION.md](DEPLOYMENT_CONFIGURATION.md#quick-start)
- **Troubleshooting:** [DEPLOYMENT_CONFIGURATION.md](DEPLOYMENT_CONFIGURATION.md#troubleshooting)
- **Security:** [DEPLOYMENT_CONFIGURATION.md](DEPLOYMENT_CONFIGURATION.md#security-checklist)
- **Maintenance:** [DEPLOYMENT_CONFIGURATION.md](DEPLOYMENT_CONFIGURATION.md#maintenance)

## 🗂️ Configuration Files

### Environment Templates

| File | Purpose | Location |
|------|---------|----------|
| `backend/.env.production.example` | Backend production configuration template | [backend/.env.production.example](backend/.env.production.example) |
| `frontend/.env.production.example` | Frontend production configuration template | [frontend/.env.production.example](frontend/.env.production.example) |

### Apache Configuration

| File | Purpose | Location |
|------|---------|----------|
| `deployment/apache/airzone.conf` | Apache virtual host configuration | [deployment/apache/airzone.conf](deployment/apache/airzone.conf) |
| `backend/wsgi.py` | WSGI entry point for Flask | [backend/wsgi.py](backend/wsgi.py) |

### Systemd Services

| File | Purpose | Location |
|------|---------|----------|
| `deployment/systemd/airzone-backend.service` | Backend systemd service | [deployment/systemd/airzone-backend.service](deployment/systemd/airzone-backend.service) |
| `deployment/systemd/airzone-frontend.service` | Frontend systemd service | [deployment/systemd/airzone-frontend.service](deployment/systemd/airzone-frontend.service) |

## 🛠️ Scripts

### Deployment Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `deployment/deploy.sh` | Complete automated deployment | `sudo bash deployment/deploy.sh` |
| `deployment/apache/setup_apache.sh` | Apache setup automation | `sudo bash deployment/apache/setup_apache.sh` |
| `deployment/systemd/setup_services.sh` | Systemd services setup | `sudo bash deployment/systemd/setup_services.sh` |
| `deployment/verify_deployment.sh` | Deployment verification | `bash deployment/verify_deployment.sh` |

### Utility Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/generate_secrets.py` | Generate secure secret keys | `python3 scripts/generate_secrets.py` |
| `scripts/generate_sponsor_wallet.py` | Generate XRPL sponsor wallet | `python3 scripts/generate_sponsor_wallet.py` |
| `scripts/setup_database.py` | Database initialization | `python3 scripts/setup_database.py` |

## 🚀 Quick Start

### Option 1: Automated Deployment (Recommended)

```bash
# Clone repository
cd /var/www && sudo git clone <repo-url> airzone
cd airzone

# Run automated deployment
sudo bash deployment/deploy.sh

# Generate secrets
python3 scripts/generate_secrets.py

# Configure environment
sudo nano backend/.env
sudo nano frontend/.env.local

# Restart services
sudo systemctl restart airzone-backend airzone-frontend
```

### Option 2: Manual Deployment

Follow the step-by-step guide in [DEPLOYMENT_CONFIGURATION.md](DEPLOYMENT_CONFIGURATION.md).

### Option 3: Quick Deploy (5 minutes)

Follow the condensed guide in [deployment/QUICK_DEPLOY.md](deployment/QUICK_DEPLOY.md).

## 📋 Deployment Workflow

```
1. Prerequisites
   ├── Install system dependencies
   ├── Configure domain DNS
   └── Prepare MySQL database

2. Application Setup
   ├── Clone repository
   ├── Setup backend (venv, dependencies)
   └── Setup frontend (npm install, build)

3. Configuration
   ├── Generate secrets
   ├── Configure backend .env
   └── Configure frontend .env.local

4. Web Server
   ├── Configure Apache
   ├── Enable modules
   └── Enable site

5. Services
   ├── Install systemd services
   ├── Enable services
   └── Start services

6. SSL/TLS
   ├── Obtain certificate
   └── Configure auto-renewal

7. Security
   ├── Configure firewall
   ├── Set file permissions
   └── Verify security headers

8. Verification
   ├── Check services
   ├── Test endpoints
   └── Review logs
```

## 🔧 Common Tasks

### Service Management

```bash
# Start services
sudo systemctl start airzone-backend airzone-frontend

# Stop services
sudo systemctl stop airzone-backend airzone-frontend

# Restart services
sudo systemctl restart airzone-backend airzone-frontend

# Check status
sudo systemctl status airzone-backend airzone-frontend

# View logs
sudo journalctl -u airzone-backend -f
sudo journalctl -u airzone-frontend -f
```

### Apache Management

```bash
# Test configuration
sudo apache2ctl configtest

# Reload configuration
sudo systemctl reload apache2

# Restart Apache
sudo systemctl restart apache2

# View logs
sudo tail -f /var/log/apache2/airzone_error.log
```

### SSL Certificate

```bash
# Obtain certificate
sudo certbot --apache -d airz.one -d www.airz.one

# Renew certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

### Application Updates

```bash
# Pull latest code
cd /var/www/airzone
sudo -u www-data git pull

# Update backend
cd backend
sudo -u www-data bash -c "source venv/bin/activate && pip install -r requirements.txt"
sudo systemctl restart airzone-backend

# Update frontend
cd ../frontend
sudo -u www-data npm install
sudo -u www-data npm run build
sudo systemctl restart airzone-frontend
```

## 🔍 Troubleshooting

### Quick Diagnostics

```bash
# Run verification script
bash deployment/verify_deployment.sh

# Check all services
sudo systemctl status apache2 airzone-backend airzone-frontend

# Check recent logs
sudo journalctl -u airzone-backend -n 50
sudo journalctl -u airzone-frontend -n 50
sudo tail -n 50 /var/log/apache2/airzone_error.log
```

### Common Issues

| Issue | Solution | Documentation |
|-------|----------|---------------|
| Backend won't start | Check logs and .env configuration | [Troubleshooting](DEPLOYMENT_CONFIGURATION.md#troubleshooting) |
| Frontend won't start | Verify build completed successfully | [Troubleshooting](DEPLOYMENT_CONFIGURATION.md#troubleshooting) |
| Apache config error | Run `apache2ctl configtest` | [Apache Issues](DEPLOYMENT_CONFIGURATION.md#apache-issues) |
| SSL certificate error | Check certbot logs | [SSL Issues](DEPLOYMENT_CONFIGURATION.md#ssl-certificate-issues) |
| Database connection | Verify credentials in .env | [Database Issues](DEPLOYMENT_CONFIGURATION.md#database-connection-issues) |

## 📊 Monitoring

### Log Locations

| Log | Location | Command |
|-----|----------|---------|
| Backend errors | `/var/log/airzone/backend-error.log` | `sudo tail -f /var/log/airzone/backend-error.log` |
| Backend access | `/var/log/airzone/backend-access.log` | `sudo tail -f /var/log/airzone/backend-access.log` |
| Frontend | systemd journal | `sudo journalctl -u airzone-frontend -f` |
| Apache errors | `/var/log/apache2/airzone_error.log` | `sudo tail -f /var/log/apache2/airzone_error.log` |
| Apache access | `/var/log/apache2/airzone_access.log` | `sudo tail -f /var/log/apache2/airzone_access.log` |

### Health Checks

```bash
# Backend health
curl http://localhost:5000/api/v1/health

# Frontend health
curl http://localhost:3000

# HTTPS check
curl -I https://airz.one

# SSL certificate check
openssl s_client -connect airz.one:443 -servername airz.one
```

## 🔒 Security

### Security Checklist

- [ ] Strong secrets generated
- [ ] .env files have 600 permissions
- [ ] HTTPS enabled with valid certificate
- [ ] HSTS headers configured
- [ ] Firewall enabled
- [ ] Database user has limited privileges
- [ ] Regular security updates scheduled

### Security Documentation

- [Security Checklist](DEPLOYMENT_CONFIGURATION.md#security-checklist)
- [Security Best Practices](DEPLOYMENT_CONFIGURATION.md#security-best-practices)
- [File Permissions](DEPLOYMENT_CONFIGURATION.md#file-permissions)

## 📦 Backup and Recovery

### Backup Commands

```bash
# Database backup
mysqldump -u airzone_user -p airzone > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf airzone_backup_$(date +%Y%m%d).tar.gz /var/www/airzone

# Configuration backup
tar -czf config_backup_$(date +%Y%m%d).tar.gz \
  /var/www/airzone/backend/.env \
  /var/www/airzone/frontend/.env.local \
  /etc/apache2/sites-available/airzone.conf \
  /etc/systemd/system/airzone-*.service
```

## 📞 Support

### Getting Help

1. **Check Documentation:** Review the relevant guide above
2. **Check Logs:** Look for error messages in logs
3. **Run Verification:** Use `verify_deployment.sh` to check configuration
4. **Review Checklist:** Ensure all steps in [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) are complete
5. **Contact Admin:** If issues persist, contact system administrator

### Useful Resources

- [Apache Documentation](https://httpd.apache.org/docs/2.4/)
- [Systemd Documentation](https://www.freedesktop.org/software/systemd/man/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

## 📝 Notes

- All scripts should be run from the appropriate directory
- Most scripts require sudo/root privileges
- Always backup before making changes
- Test in staging environment first
- Keep documentation updated

---

**Last Updated:** 2024
**Version:** 1.0
**Status:** Production Ready
