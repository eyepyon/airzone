# Getting Started with Airzone

Complete guide to setting up the Airzone development environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/)

## Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd airzone
```

### Step 2: Database Setup

#### Quick Setup (Recommended)

```bash
# Windows
DATABASE_QUICK_SETUP.bat

# Linux/Mac
bash DATABASE_QUICK_SETUP.sh
```

#### Manual Setup

1. **Configure environment variables:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your MySQL credentials
   ```

2. **Run database initialization:**
   ```bash
   python init_db.py
   ```

3. **Apply migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Seed test data:**
   ```bash
   cd ..
   python scripts/seed_data.py
   ```

5. **Verify setup:**
   ```bash
   cd backend
   python verify_database.py
   ```

For detailed instructions, see [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)

### Step 3: Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   
   Edit `backend/.env` with your configuration:
   ```env
   # Flask
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   
   # Database (already configured in Step 2)
   DB_HOST=localhost
   DB_NAME=airzone
   DB_USER=airzone_user
   DB_PASSWORD=your-password
   
   # Google OAuth
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   
   # Stripe
   STRIPE_SECRET_KEY=your-stripe-secret
   STRIPE_PUBLISHABLE_KEY=your-stripe-publishable
   STRIPE_WEBHOOK_SECRET=your-webhook-secret
   
   # XRPL Blockchain
   XRPL_NETWORK=testnet
   XRPL_SPONSOR_SEED=your-sponsor-seed
   
   # Security
   ENCRYPTION_KEY=your-encryption-key
   ```

3. **Start the backend server:**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Step 4: Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-client-id
   NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your-stripe-key
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

### Step 5: Smart Contract Deployment (Optional)

If you want to deploy your own smart contract:

1. **Install XRPL CLI:**

2. **Deploy the contract:**
   ```bash
   bash scripts/deploy_contract.sh testnet
   ```

3. **Update backend configuration:**
   Add the package ID to `backend/.env`:
   ```env
   SUI_PACKAGE_ID=0x...
   ```

For detailed instructions, see [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)

## Verification

### Check Backend

```bash
# Test API health
curl http://localhost:5000/api/v1/health

# Check database connection
cd backend
python verify_database.py
```

### Check Frontend

1. Open `http://localhost:3000` in your browser
2. You should see the Airzone homepage
3. Try navigating to different pages

### Check Database

```bash
# Connect to MySQL
mysql -u airzone_user -p airzone

# Check tables
SHOW TABLES;

# Check products
SELECT id, name, price FROM products;
```

## Common Issues

### Database Connection Failed

**Problem:** Can't connect to MySQL

**Solution:**
1. Ensure MySQL is running
2. Verify credentials in `backend/.env`
3. Check MySQL is listening on port 3306
4. Try connecting manually: `mysql -u airzone_user -p`

### Port Already in Use

**Problem:** Port 5000 or 3000 is already in use

**Solution:**
```bash
# Backend - change port in app.py or use:
python app.py --port 5001

# Frontend - change port:
npm run dev -- -p 3001
```

### Module Not Found

**Problem:** Python or Node.js modules not found

**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Migration Errors

**Problem:** Alembic migration fails

**Solution:**
```bash
cd backend

# Check current version
alembic current

# Force to head
alembic stamp head

# Retry migration
alembic upgrade head
```

## Development Workflow

### Making Database Changes

1. Modify models in `backend/models/`
2. Create migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "description"
   ```
3. Review migration file in `backend/alembic/versions/`
4. Apply migration:
   ```bash
   alembic upgrade head
   ```

### Testing the Application

1. **Backend tests:**
   ```bash
   cd backend
   pytest
   ```

2. **Frontend tests:**
   ```bash
   cd frontend
   npm test
   ```

### Resetting the Database

```bash
# Drop all tables
cd backend
alembic downgrade base

# Recreate tables
alembic upgrade head

# Reseed data
cd ..
python scripts/seed_data.py
```

## Next Steps

After setup is complete:

1. **Configure OAuth:**
   - Set up Google OAuth credentials
   - Update `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

2. **Configure Stripe:**
   - Create Stripe account
   - Get API keys
   - Set up webhook endpoint

3. **Setup XRPL:**
   - Generate sponsor wallet
   - Fund with test XRP
   - Verify connection

4. **Test the Flow:**
   - Register a user
   - Mint an NFT
   - Browse products
   - Make a purchase

## Additional Resources

- **Database Setup:** [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)
- **Backend API:** [backend/README.md](backend/README.md)
- **Frontend:** [frontend/README.md](frontend/README.md)
- **Smart Contracts:** [contracts/README.md](contracts/README.md)
- **Deployment:** [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)

## Support

For issues or questions:

1. Check the troubleshooting sections in documentation
2. Review error messages carefully
3. Verify all prerequisites are met
4. Check environment variables are set correctly

## Quick Reference

### Start Development

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Access Points

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Docs: http://localhost:5000/api/v1/docs (if configured)

### Environment Files

- Backend: `backend/.env`
- Frontend: `frontend/.env.local`

### Key Commands

```bash
# Database
python scripts/setup_database.py
cd backend && python verify_database.py

# Backend
cd backend && python app.py

# Frontend
cd frontend && npm run dev

# Migrations
cd backend && alembic upgrade head

# Tests
cd backend && pytest
cd frontend && npm test
```

---

**Ready to start developing!** 🚀
