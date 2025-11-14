# Database Setup Guide

This guide provides detailed instructions for setting up the MySQL database for the Airzone application.

## Prerequisites

- MySQL 8.0 or higher installed and running
- Python 3.11+ installed
- Required Python packages installed (`pip install -r requirements.txt`)

## Quick Setup (Automated)

The easiest way to set up the database is using the automated setup script:

```bash
# From the project root directory
python scripts/setup_database.py
```

This script will:
1. Create the MySQL database (`airzone`)
2. Create the database user (`airzone_user`)
3. Grant necessary privileges
4. Run Alembic migrations to create all tables
5. Seed initial test data

## Manual Setup

If you prefer to set up the database manually, follow these steps:

### Step 1: Configure Environment Variables

Create or update `backend/.env` with your database credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airzone
DB_USER=airzone_user
DB_PASSWORD=your-secure-password

# Database Root Credentials (for initial setup only)
DB_ROOT_USER=root
DB_ROOT_PASSWORD=your-root-password
```

### Step 2: Create Database and User

Run the database initialization script:

```bash
cd backend
python init_db.py
```

This will:
- Create the `airzone` database if it doesn't exist
- Create the `airzone_user` user if it doesn't exist
- Grant all privileges on the `airzone` database to `airzone_user`

### Step 3: Run Migrations

Apply the database schema using Alembic:

```bash
cd backend
alembic upgrade head
```

This creates all the necessary tables:
- `users` - User accounts
- `wallets` - Sui blockchain wallets
- `nft_mints` - NFT minting records
- `products` - E-commerce products
- `orders` - Customer orders
- `order_items` - Order line items
- `payments` - Payment transactions
- `wifi_sessions` - WiFi connection sessions
- `task_queue` - Background task queue

### Step 4: Seed Initial Data

Populate the database with test data:

```bash
python scripts/seed_data.py
```

This adds sample products to the database for testing.

## Verification

Verify that the database is properly set up:

```bash
python backend/verify_database.py
```

This script checks:
- Database connection
- All tables exist
- Migration version
- Data counts
- Sample data

## Database Schema

### Tables Overview

| Table | Description |
|-------|-------------|
| `users` | User accounts with Google OAuth authentication |
| `wallets` | Sui blockchain wallet addresses and encrypted private keys |
| `nft_mints` | NFT minting operations and status tracking |
| `products` | E-commerce products with optional NFT requirements |
| `orders` | Customer orders with status tracking |
| `order_items` | Individual items within orders |
| `payments` | Stripe payment transactions |
| `wifi_sessions` | WiFi captive portal connection sessions |
| `task_queue` | Background task management with retry logic |

### Key Relationships

- `users` → `wallets` (one-to-many)
- `users` → `nft_mints` (one-to-many)
- `users` → `orders` (one-to-many)
- `users` → `wifi_sessions` (one-to-many)
- `orders` → `order_items` (one-to-many)
- `orders` → `payments` (one-to-many)
- `products` ← `order_items` (many-to-one)

## Troubleshooting

### Connection Refused

If you get a connection refused error:

1. Ensure MySQL is running:
   ```bash
   # Windows
   net start MySQL80
   
   # Linux/Mac
   sudo systemctl start mysql
   ```

2. Check MySQL is listening on the correct port:
   ```bash
   netstat -an | findstr 3306
   ```

### Access Denied

If you get an access denied error:

1. Verify your root credentials in `backend/.env`
2. Try connecting manually:
   ```bash
   mysql -u root -p
   ```

### Migration Errors

If migrations fail:

1. Check the current migration version:
   ```bash
   cd backend
   alembic current
   ```

2. View migration history:
   ```bash
   alembic history
   ```

3. Reset migrations (WARNING: This will drop all tables):
   ```bash
   alembic downgrade base
   alembic upgrade head
   ```

### Table Already Exists

If you get "table already exists" errors:

1. Check if tables were created outside of Alembic
2. Either drop the tables manually or stamp the current version:
   ```bash
   alembic stamp head
   ```

## Database Maintenance

### Backup Database

```bash
mysqldump -u airzone_user -p airzone > backup.sql
```

### Restore Database

```bash
mysql -u airzone_user -p airzone < backup.sql
```

### Reset Database

To completely reset the database:

```bash
# Drop and recreate database
mysql -u root -p -e "DROP DATABASE IF EXISTS airzone; CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run setup again
python scripts/setup_database.py
```

## Production Considerations

For production deployment:

1. **Use strong passwords** for database users
2. **Enable SSL/TLS** for database connections
3. **Configure backups** with automated scheduling
4. **Set up monitoring** for database performance
5. **Limit privileges** - don't use root in production
6. **Use connection pooling** (already configured in SQLAlchemy)
7. **Enable slow query logging** for optimization

## Additional Resources

- [MySQL 8.0 Documentation](https://dev.mysql.com/doc/refman/8.0/en/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
