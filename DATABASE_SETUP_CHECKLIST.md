# Database Setup Checklist

Use this checklist to ensure all database setup steps are completed correctly.

## Pre-Setup

- [ ] MySQL 8.0+ is installed
- [ ] MySQL service is running
- [ ] Python 3.11+ is installed
- [ ] Backend dependencies are installed (`pip install -r backend/requirements.txt`)
- [ ] You have MySQL root credentials

## Configuration

- [ ] `backend/.env` file exists (copied from `.env.example`)
- [ ] `DB_ROOT_USER` is set in `backend/.env`
- [ ] `DB_ROOT_PASSWORD` is set in `backend/.env`
- [ ] `DB_NAME` is set (default: `airzone`)
- [ ] `DB_USER` is set (default: `airzone_user`)
- [ ] `DB_PASSWORD` is set (secure password for airzone_user)
- [ ] `DB_HOST` is set (default: `localhost`)
- [ ] `DB_PORT` is set (default: `3306`)

## Database Creation

- [ ] Database `airzone` has been created
- [ ] User `airzone_user` has been created
- [ ] User has been granted privileges on `airzone` database
- [ ] Can connect to database with `airzone_user` credentials

**Verify with:**
```bash
python backend/init_db.py
```

## Schema Migration

- [ ] Alembic is configured (`backend/alembic.ini` exists)
- [ ] Alembic env.py is configured (`backend/alembic/env.py` exists)
- [ ] Initial migration file exists (`backend/alembic/versions/001_initial_schema.py`)
- [ ] Migrations have been applied successfully
- [ ] All 9 tables have been created:
  - [ ] `users`
  - [ ] `wallets`
  - [ ] `nft_mints`
  - [ ] `products`
  - [ ] `orders`
  - [ ] `order_items`
  - [ ] `payments`
  - [ ] `wifi_sessions`
  - [ ] `task_queue`
- [ ] `alembic_version` table exists with current version

**Verify with:**
```bash
cd backend
alembic current
alembic history
```

## Data Seeding

- [ ] Seed script exists (`scripts/seed_data.py`)
- [ ] Seed script has been executed successfully
- [ ] Products table contains test data (8 sample products)
- [ ] Sample products include both public and NFT-gated items

**Verify with:**
```bash
python scripts/seed_data.py
```

## Verification

- [ ] Database connection test passes
- [ ] All expected tables exist
- [ ] Migration version is correct
- [ ] Data counts are as expected
- [ ] Sample products are visible

**Verify with:**
```bash
python backend/verify_database.py
```

## Post-Setup

- [ ] Database credentials are secure (not using default passwords)
- [ ] Root credentials are removed from `.env` (or file is secured)
- [ ] Database backup strategy is planned
- [ ] Connection pooling is configured (default in SQLAlchemy)
- [ ] Database monitoring is set up (optional for development)

## Testing

- [ ] Can start Flask application without database errors
- [ ] Can query users table via API
- [ ] Can query products table via API
- [ ] Can create test user via API
- [ ] Can create test order via API

**Test with:**
```bash
cd backend
python app.py
# In another terminal:
curl http://localhost:5000/api/v1/products
```

## Troubleshooting Completed

If you encountered issues, mark what you resolved:

- [ ] Fixed MySQL connection issues
- [ ] Fixed authentication/permission issues
- [ ] Fixed migration errors
- [ ] Fixed seeding errors
- [ ] Fixed table creation issues
- [ ] Other: ___________________________

## Documentation Review

- [ ] Read `backend/DATABASE_SETUP.md`
- [ ] Read `backend/DATABASE_QUICK_START.md`
- [ ] Understand database schema
- [ ] Understand migration process
- [ ] Know how to backup/restore database

## Ready for Development

- [ ] All checklist items above are complete
- [ ] Database is accessible from application
- [ ] Sample data is available for testing
- [ ] Team members can access database (if applicable)
- [ ] Development environment is fully configured

---

## Quick Commands Reference

```bash
# Full automated setup
python scripts/setup_database.py

# Or manual steps:
python backend/init_db.py                    # Create DB and user
cd backend && alembic upgrade head           # Run migrations
python scripts/seed_data.py                  # Seed data
python backend/verify_database.py            # Verify setup

# Verification
python backend/verify_database.py

# Reset database (if needed)
mysql -u root -p -e "DROP DATABASE IF EXISTS airzone;"
python scripts/setup_database.py
```

---

**Setup Date:** _______________  
**Setup By:** _______________  
**Environment:** [ ] Development [ ] Staging [ ] Production  
**Notes:** _______________________________________________
