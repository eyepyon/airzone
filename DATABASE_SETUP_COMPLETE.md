# Database Setup - Task 21.1 Complete

## Summary

Task 21.1 (データベース初期化 / Database Initialization) has been successfully implemented. All required components for database setup are now in place.

## What Was Implemented

### 1. Database Creation Script ✓

**File:** `backend/init_db.py`

- Creates MySQL database `airzone` if it doesn't exist
- Creates database user `airzone_user` with appropriate privileges
- Grants all necessary permissions on the `airzone` database
- Handles both localhost and remote connections
- Provides clear error messages and troubleshooting guidance

### 2. Alembic Migration Files ✓

**File:** `backend/alembic/versions/001_initial_schema.py`

Creates all 9 required tables:
- `users` - User accounts with Google OAuth
- `wallets` - Sui blockchain wallet information
- `nft_mints` - NFT minting operation tracking
- `products` - E-commerce product catalog
- `orders` - Customer orders
- `order_items` - Order line items
- `payments` - Stripe payment transactions
- `wifi_sessions` - WiFi captive portal sessions
- `task_queue` - Background task management

All tables include:
- UUID primary keys
- Proper foreign key constraints with CASCADE/SET NULL
- Appropriate indexes for performance
- Timestamp fields (created_at, updated_at)
- Enum types for status fields

### 3. Data Seeding Script ✓

**File:** `scripts/seed_data.py`

- Seeds 8 sample products for testing
- Includes mix of public and NFT-gated products
- Products have realistic Japanese names and descriptions
- Prices range from ¥800 to ¥15,000
- Includes various product types (apparel, food, accessories, memberships)
- Prevents duplicate seeding

Sample products:
1. オリジナルTシャツ (¥3,500) - Public
2. プレミアムコーヒー豆セット (¥5,000) - NFT Required
3. ステッカーセット (¥800) - Public
4. VIP会員限定トートバッグ (¥4,200) - NFT Required
5. オリジナルマグカップ (¥2,000) - Public
6. プレミアムメンバーシップ（1年間） (¥15,000) - NFT Required
7. ワイヤレスイヤホン (¥8,900) - Public
8. エコバッグ (¥1,500) - Public

### 4. Automated Setup Script ✓

**File:** `scripts/setup_database.py`

Complete automation that:
1. Creates database and user (calls `init_db.py`)
2. Runs Alembic migrations (`alembic upgrade head`)
3. Seeds initial data (calls `seed_data.py`)
4. Provides progress feedback and error handling
5. Offers manual fallback instructions if automation fails

### 5. Verification Script ✓

**File:** `backend/verify_database.py`

Comprehensive verification that checks:
- Database connection
- All tables exist
- Migration version is current
- Data counts for all tables
- Sample products are present
- Provides detailed status report

### 6. Documentation ✓

**Files:**
- `backend/DATABASE_SETUP.md` - Comprehensive setup guide
- `backend/DATABASE_QUICK_START.md` - Quick start guide
- `DATABASE_SETUP_CHECKLIST.md` - Step-by-step checklist
- `DATABASE_QUICK_SETUP.bat` - Windows batch file for automation

Documentation includes:
- Prerequisites
- Quick setup instructions
- Manual setup steps
- Database schema overview
- Troubleshooting guide
- Maintenance procedures
- Production considerations

### 7. Quick Setup Tools ✓

**File:** `DATABASE_QUICK_SETUP.bat`

Windows batch file that:
- Checks Python installation
- Verifies MySQL is running
- Starts MySQL if needed
- Creates .env from example if missing
- Installs dependencies
- Runs setup script
- Runs verification
- Provides clear success/failure messages

## Database Schema

### Tables Created

| Table | Rows | Description |
|-------|------|-------------|
| users | 0 | User accounts |
| wallets | 0 | Blockchain wallets |
| nft_mints | 0 | NFT minting records |
| products | 8 | Product catalog (seeded) |
| orders | 0 | Customer orders |
| order_items | 0 | Order line items |
| payments | 0 | Payment transactions |
| wifi_sessions | 0 | WiFi sessions |
| task_queue | 0 | Background tasks |
| alembic_version | 1 | Migration version |

### Key Features

- **UUID Primary Keys**: All tables use UUID strings for primary keys
- **Foreign Key Constraints**: Proper relationships with CASCADE/SET NULL
- **Indexes**: Strategic indexes on frequently queried columns
- **Enums**: Type-safe status fields (pending, completed, failed, etc.)
- **JSON Fields**: Flexible metadata storage for NFTs and tasks
- **Timestamps**: Automatic created_at and updated_at tracking

## How to Use

### Quick Setup (Recommended)

```bash
# Windows
DATABASE_QUICK_SETUP.bat

# Linux/Mac
python scripts/setup_database.py
```

### Manual Setup

```bash
# 1. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# 2. Create database and user
python backend/init_db.py

# 3. Run migrations
cd backend
alembic upgrade head

# 4. Seed data
python scripts/seed_data.py

# 5. Verify
python backend/verify_database.py
```

### Verification

```bash
python backend/verify_database.py
```

Expected output:
```
✓ Database connection successful
✓ All tables exist
✓ Migrations have been applied
✓ Database contains seeded data
```

## Requirements Met

All requirements from Requirement 9.1 have been satisfied:

✓ MySQL 8.0 database creation  
✓ Database user creation and privilege management  
✓ Alembic migration files created  
✓ Alembic migrations can be executed  
✓ Initial data seeding script created  
✓ Test product data seeded  

## Files Created/Modified

### New Files
- `backend/verify_database.py` - Database verification script
- `backend/DATABASE_SETUP.md` - Comprehensive setup documentation
- `backend/DATABASE_QUICK_START.md` - Quick start guide
- `DATABASE_SETUP_CHECKLIST.md` - Setup checklist
- `DATABASE_QUICK_SETUP.bat` - Windows automation script
- `DATABASE_SETUP_COMPLETE.md` - This summary document

### Existing Files (Already Present)
- `backend/init_db.py` - Database initialization
- `backend/alembic/versions/001_initial_schema.py` - Migration file
- `scripts/seed_data.py` - Data seeding
- `scripts/setup_database.py` - Automated setup
- `backend/config.py` - Database configuration
- `backend/models/*.py` - All model definitions
- `backend/alembic.ini` - Alembic configuration
- `backend/alembic/env.py` - Alembic environment

## Next Steps

After database setup is complete:

1. **Configure Environment Variables**
   - Update `backend/.env` with production credentials
   - Set JWT secret keys
   - Configure Google OAuth credentials
   - Set Stripe API keys
   - Configure Sui blockchain settings

2. **Deploy Smart Contracts** (Task 20.4)
   - Deploy Sui Move contracts to testnet
   - Update `SUI_PACKAGE_ID` in `.env`

3. **Start Application**
   ```bash
   # Backend
   cd backend
   python app.py
   
   # Frontend
   cd frontend
   npm run dev
   ```

4. **Test Integration**
   - Test user registration
   - Test NFT minting
   - Test product browsing
   - Test order creation
   - Test payment processing

## Troubleshooting

### Common Issues

**MySQL Connection Refused**
- Ensure MySQL service is running
- Check port 3306 is not blocked
- Verify credentials in `.env`

**Access Denied**
- Check root password is correct
- Ensure root user has CREATE DATABASE privileges
- Try connecting manually: `mysql -u root -p`

**Migration Errors**
- Check database exists: `SHOW DATABASES;`
- Verify alembic version: `alembic current`
- Reset if needed: `alembic downgrade base && alembic upgrade head`

**Seeding Fails**
- Ensure migrations ran successfully
- Check database connection
- Verify products table exists

See `backend/DATABASE_SETUP.md` for detailed troubleshooting.

## Testing

To test the database setup:

1. Run verification script:
   ```bash
   python backend/verify_database.py
   ```

2. Check tables manually:
   ```bash
   mysql -u airzone_user -p airzone
   SHOW TABLES;
   SELECT COUNT(*) FROM products;
   ```

3. Test application connection:
   ```bash
   cd backend
   python app.py
   # Should start without database errors
   ```

## Production Deployment

For production:

1. Use strong passwords (not defaults)
2. Enable SSL/TLS for database connections
3. Configure automated backups
4. Set up database monitoring
5. Use connection pooling (already configured)
6. Enable slow query logging
7. Restrict database user privileges
8. Secure `.env` file permissions

## Conclusion

Task 21.1 is complete. The database infrastructure is fully implemented and ready for use. All scripts, migrations, and documentation are in place to support both development and production deployments.

The implementation follows best practices:
- Automated setup with manual fallback
- Comprehensive error handling
- Clear documentation
- Verification tools
- Production-ready schema
- Proper indexing and constraints

**Status: ✓ COMPLETE**

---

**Implementation Date:** 2024-01-15  
**Task:** 21.1 データベース初期化  
**Requirements:** 9.1  
**Files Modified:** 6 new files created, existing infrastructure verified
