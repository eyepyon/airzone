# Database Quick Start

Get your Airzone database up and running in 3 simple steps!

## Prerequisites

✓ MySQL 8.0+ installed and running  
✓ Python 3.11+ installed  
✓ Dependencies installed: `pip install -r backend/requirements.txt`

## Quick Setup

### 1. Configure Environment

Copy the example environment file and update with your credentials:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and set:
```env
DB_ROOT_USER=root
DB_ROOT_PASSWORD=your_mysql_root_password
DB_PASSWORD=your_secure_password_for_airzone_user
```

### 2. Run Setup Script

From the project root:

```bash
python scripts/setup_database.py
```

This automatically:
- Creates the `airzone` database
- Creates the `airzone_user` user
- Runs all migrations
- Seeds test data

### 3. Verify Setup

```bash
python backend/verify_database.py
```

You should see:
```
✓ Database connection successful
✓ All tables exist
✓ Migrations have been applied
✓ Database contains seeded data
```

## That's It!

Your database is ready. Start the application:

```bash
# Backend
cd backend
python app.py

# Frontend (in another terminal)
cd frontend
npm run dev
```

## Troubleshooting

**MySQL not running?**
```bash
# Windows
net start MySQL80

# Linux/Mac
sudo systemctl start mysql
```

**Connection issues?**
- Check MySQL is on port 3306
- Verify credentials in `backend/.env`
- Ensure root user has CREATE DATABASE privileges

**Need to reset?**
```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS airzone;"
python scripts/setup_database.py
```

## What Was Created?

- **Database**: `airzone`
- **User**: `airzone_user` (with full privileges)
- **Tables**: 9 tables (users, wallets, nft_mints, products, orders, etc.)
- **Sample Data**: 8 test products

## Next Steps

1. Update other environment variables in `backend/.env`:
   - `JWT_SECRET_KEY`
   - `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
   - `STRIPE_SECRET_KEY`
   - `SUI_SPONSOR_PRIVATE_KEY`

2. Deploy smart contracts (see `contracts/README.md`)

3. Start building!

## Need More Details?

See `backend/DATABASE_SETUP.md` for comprehensive documentation.
