# Airzone

Japanese README:  
https://github.com/eyepyon/airzone/blob/main/README_JP.md  
 

WiFi-triggered NFT distribution and e-commerce shop platform powered by XRPL (XRP Ledger) blockchain.

## Overview

Airzone is a next-generation platform that automatically distributes NFTs when users connect to WiFi and enables NFT-gated product sales. Using the XRPL (XRP Ledger) blockchain, it provides fast and low-cost NFT minting with innovative user experiences.

## 🚀 Key Features

### 🎯 Core Features
- **WiFi-Triggered NFT Distribution**: Automatic NFT minting when connecting to specific WiFi
- **Google OAuth Authentication**: Easy user registration and login
- **Automatic Wallet Generation**: Auto-create XRPL wallets on user registration
- **Xaman Wallet Support**: Users can connect their own Xaman Wallet
- **NFT-Gated Products**: Products purchasable only by NFT holders
- **Stripe Payment**: Credit card payment support

### 🎁 Referral & Reward System
- **Referral Links**: Invite friends and earn coins
- **SNS Sharing**: One-click sharing on Twitter, LINE, Facebook
- **Exclusive Product Access**: Referred users can purchase exclusive products
- **Coin Rewards**: Earn 100 coins per successful referral

### 💎 Staking Features
- **XRP Escrow Staking**: Lock XRP for a period to earn exclusive NFTs
- **Automatic Release**: Auto-receive XRP and NFTs after the period ends
- **Campaign Management**: Run multiple staking campaigns simultaneously

### 👑 User Importance System
- **Score Calculation**: Auto-calculate importance from purchases, referrals, logins, etc.
- **5-Tier Levels**: Bronze, Silver, Gold, Platinum, Diamond
- **VIP Benefits**: Special perks for high-level users

### 💸 Batch Transfer System
- **XRPL Batch Transactions**: Efficient bulk XRP transfers using Tickets
- **Parallel Processing**: Send to multiple users simultaneously
- **Flexible Targeting**: Send to specific users, VIPs, or top referrers
- **Complete History**: Full transaction tracking and audit trail

### 📊 Management & Analytics
- **Admin Panel**: Comprehensive management of users, products, orders, NFTs
- **Analytics Dashboard**: Visualize DAU, MAU, downloads, and other metrics
- **Referral Management**: View referral statistics, rankings, and detailed history
- **User Importance Management**: User importance rankings and detailed analysis
- **Batch Transfer Management**: Monitor and execute bulk XRP distributions

## 🔥 Feature Highlights

### 🎁 Referral Link System

Invite friends to earn coins, and referred users get access to exclusive products:

- **Referral Code Generation**: 8-character unique codes
- **SNS Sharing**: One-click posting to Twitter, LINE, Facebook
- **Coin Rewards**: Earn 100 coins per successful referral
- **Exclusive Products**: Special products for referred users
- **Click Tracking**: Record referral link clicks

Details: [Referral System Guide](docs/REFERRAL_SYSTEM_JP.md)

### 💎 XRP Escrow Staking

Revolutionary staking system using XRPL's Escrow feature:

- **True Locking**: XRP is actually locked on the blockchain
- **Automatic Release**: Auto-receive XRP and NFTs after period ends
- **Exclusive NFTs**: Issue NFTs exclusive to staking participants
- **Transparency**: Everything verifiable on the blockchain
- **Security**: Highest level security with XRPL native features

Details: [Escrow Staking Guide](docs/ESCROW_STAKING_JP.md)

### 👑 User Importance Score

Comprehensive user evaluation system:

- **Multi-faceted Evaluation**: Multiple metrics including purchases, referrals, logins, NFT minting
- **Auto-calculation**: Real-time score updates
- **5-Tier Levels**: 🥉Bronze → 🥈Silver → 🥇Gold → 💎Platinum → 👑Diamond
- **VIP Benefits**: Special perks and services based on level
- **Rankings**: Visualize top users

Details: [User Importance System Guide](docs/USER_IMPORTANCE_SYSTEM_JP.md)

### 💸 Batch Transfer System

Efficient bulk XRP distribution using XRPL's Batch Transactions:

- **Ticket-based**: Use XRPL Tickets for parallel transaction processing
- **High Performance**: Send to 100+ users in seconds
- **Low Cost**: Same fee as regular transactions (~0.00001 XRP/tx)
- **Flexible Targeting**: Send to specific users, VIP levels, or top referrers
- **Complete Audit Trail**: Full transaction history and tracking

Details: [Batch Transfer Guide](docs/BATCH_TRANSFER_JP.md)

### 📊 Advanced Analytics

- **Metrics**: Auto-measure DAU, MAU, engagement rates
- **Referral Analytics**: Referral count, click count, conversion rates
- **User Analytics**: Behavior pattern analysis by importance level
- **Real-time**: All metrics updated in real-time

## 🔗 Wallet Integration

### Auto Wallet vs Xaman Wallet

| Feature | Auto Wallet | Xaman Wallet |
|---------|-------------|--------------|
| Generation | Automatic | User connects |
| Private Key Management | Backend | User |
| Security | Standard | Highest |
| Ease of Use | ★★★★★ | ★★★☆☆ |
| Recommended For | Beginners | Security-focused |

### Documentation

- **For Users**: [Wallet Management Guide](docs/WALLET_GUIDE_JP.md)
- **For Developers**: [Xaman Wallet Integration Guide](docs/xaman-wallet-integration.md)

## 🏗️ Project Structure

```
airzone/
├── backend/          # Flask API server
│   ├── clients/      # XRPL, Stripe, Google OAuth clients
│   ├── services/     # Business logic (NFT, referral, staking, etc.)
│   ├── routes/       # API endpoints
│   └── models/       # Data models
├── frontend/         # Next.js web application
│   ├── components/   # React components
│   ├── lib/          # Utilities (Xaman Wallet, etc.)
│   └── stores/       # State management
├── admin/            # Laravel admin panel
│   ├── app/Http/Controllers/Admin/  # Admin controllers
│   └── resources/views/admin/       # Admin views
├── scripts/          # Deployment and utility scripts
└── docs/             # Documentation
```

## 💻 Technology Stack

### Backend
- **Framework**: Flask 3.0 + Python 3.11+
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT + Google OAuth 2.0
- **Blockchain**: XRPL (xrpl-py)
- **Payment**: Stripe Python SDK
- **Task Management**: Custom task manager

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Wallet**: Xaman Wallet SDK

### Blockchain
- **Main Chain**: XRPL (XRP Ledger)
- **Features**: Native NFT, Escrow, Batch Transactions, Fast transactions
- **Cost**: ~0.00001 XRP/transaction
- **Confirmation Time**: 3-5 seconds

### Database & Infrastructure
- **Database**: MySQL 8.0
- **Admin Panel**: Laravel 10 + PHP 8.1
- **Web Server**: Apache 2.4
- **SSL/TLS**: Let's Encrypt

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd airzone
```

### 2. Database Setup

```bash
mysql -u root -p
```

```sql
CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
mysql -u airzone_user -p airzone < backend/setup_database.sql
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with required settings

### 4. Generate XRPL Sponsor Wallet

```bash
python ../scripts/generate_sponsor_wallet.py
```

Add generated seed to `.env`:

```env
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 5. Get Testnet Funds

https://xrpl.org/xrp-testnet-faucet.html

### 6. Start Backend Server

```bash
python app.py
```

### 7. Frontend Setup

```bash
cd ../frontend
npm install
cp .env.local.example .env.local
npm run dev
```

### 8. Admin Panel Setup

```bash
cd ../admin
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve
```

## Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Admin Panel**: http://localhost:8000

## 🎯 Key API Endpoints

### Authentication
- `POST /api/v1/auth/google` - Google OAuth authentication
- `POST /api/v1/auth/refresh` - Token refresh

### NFT
- `GET /api/v1/nfts` - Get NFT list
- `POST /api/v1/nfts/mint` - Mint NFT

### Referral System
- `GET /api/v1/referral/code` - Get referral code
- `POST /api/v1/referral/register` - Register via referral
- `GET /api/v1/referral/stats` - Get referral statistics

### Escrow Staking
- `GET /api/v1/escrow/campaigns` - Get campaign list
- `POST /api/v1/escrow/stake` - Create stake
- `GET /api/v1/escrow/my-stakes` - Get my stakes

### User Importance
- `GET /api/v1/users/importance` - Get importance score
- `GET /api/v1/users/importance/ranking` - Get rankings

### Batch Transfer
- `POST /api/v1/batch-transfer/send` - Send to specific users
- `POST /api/v1/batch-transfer/send-to-vip` - Send to VIP users
- `POST /api/v1/batch-transfer/send-to-top-referrers` - Send to top referrers
- `POST /api/v1/batch-transfer/preview` - Preview before sending
- `GET /api/v1/batch-transfer/history` - Get transfer history

Details: [API Reference](backend/API_REFERENCE.md)

## 💡 Use Cases

### 🏪 For Stores & Facilities
- **Cafes & Restaurants**: Distribute NFT coupons via WiFi
- **Hotels & Inns**: Commemorative NFTs and repeat customer benefits
- **Event Venues**: Participation proof NFTs and exclusive merchandise
- **Shopping Malls**: Visit point NFTs and VIP membership

### 🎯 Marketing Applications
- **Brand Awareness**: Brand experience through NFTs
- **Customer Loyalty**: Tiered benefits and VIP programs
- **Viral Marketing**: Spread through referral system
- **Data Analysis**: Detailed customer behavior analysis

### 💰 Revenue Models
- **NFT-Exclusive Products**: High-value product sales
- **Staking Fees**: Escrow campaign operation fees
- **VIP Membership**: Premium service offerings
- **Data Utilization**: Anonymized behavior data analysis

## 🔧 System Requirements

### Required Environment
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **MySQL**: 8.0 or higher
- **PHP**: 8.1 or higher (for admin panel)
- **Composer**: Latest version (for admin panel)

### Recommended Specs
- **CPU**: 2+ cores
- **Memory**: 4GB+
- **Storage**: 20GB+
- **Network**: Stable internet connection

## 🌐 External Services

Required service accounts and API keys:

### Required Services
- **Google OAuth**: User authentication
- **Stripe**: Payment processing
- **XRPL**: NFT minting and staking (Testnet/Mainnet)

### Optional Services
- **Xaman Wallet**: Advanced wallet features
- **IPFS**: NFT metadata storage (recommended)
- **CDN**: Image and static file delivery

## 📚 Documentation

### 🚀 Setup
- [Complete Setup Guide](docs/SETUP_GUIDE_JP.md) - Detailed installation instructions
- [Quick Start](GETTING_STARTED_JP.md) - Get started quickly
- [Documentation Index](docs/INDEX_JP.md) - All documentation list

### 🏗️ Architecture
- [System Architecture](ARCHITECTURE_JP.md) - Overall design and tech stack

### 🔗 Blockchain
- [XRPL Integration Guide](docs/xrpl-integration.md) - XRPL basics and integration
- [Xaman Wallet Integration](docs/xaman-wallet-integration.md) - Developer details
- [Wallet Management Guide](docs/WALLET_GUIDE_JP.md) - User guide
- [Escrow Staking](docs/ESCROW_STAKING_JP.md) - XRP staking features
- [Batch Transfer](docs/BATCH_TRANSFER_JP.md) - Bulk XRP distribution
- [Blockchain Migration](BLOCKCHAIN_MIGRATION.md) - Migration details

### 🎁 Feature Guides
- [Referral System](docs/REFERRAL_SYSTEM_JP.md) - Referral link details
- [User Importance System](docs/USER_IMPORTANCE_SYSTEM_JP.md) - Score calculation system
- [Analytics Dashboard](docs/analytics-dashboard.md) - DAU/MAU analysis

### 🛠️ Management
- [Admin Panel Guide](admin/README.md) - Admin interface usage
- [Admin Panel Installation](admin/INSTALL.md) - Setup instructions

### 📡 API
- [API Reference](backend/API_REFERENCE.md) - Endpoint details

### 🔗 Other
- [Quick Links](docs/QUICK_LINKS.md) - Frequently used links
- [Documentation List](docs/README.md) - English version index

## 🛡️ Security

### Implemented Security Features
- **JWT Authentication**: Access token + refresh token
- **CORS Configuration**: Cross-origin request control
- **Rate Limiting**: API call restrictions
- **Input Validation**: Input validation on all endpoints
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **XSS Protection**: Output escaping
- **Secret Key Management**: Environment variable management

### Blockchain Security
- **Escrow Feature**: XRPL native secure locking
- **Transaction Signing**: Signature verification with private keys
- **Wallet Isolation**: Independent wallets per user

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check MySQL connection
mysql -u airzone_user -p airzone

# Run migrations
mysql -u airzone_user -p airzone < backend/setup_database.sql
```

#### XRPL Connection Error
```bash
# Check sponsor wallet
python scripts/generate_sponsor_wallet.py

# Get testnet funds
# https://xrpl.org/xrp-testnet-faucet.html
```

#### Referral System Not Working
```bash
# Run migration
mysql -u airzone_user -p airzone < backend/database/migrations/add_referral_system.sql
```

#### Escrow Staking Not Working
```bash
# Run migration
mysql -u airzone_user -p airzone < backend/database/migrations/add_escrow_campaigns.sql
```

#### Batch Transfer Not Working
```bash
# Run migration
mysql -u airzone_user -p airzone < backend/database/migrations/add_batch_transfers.sql
```

### Check Logs
- **Backend**: `backend/logs/app.log`
- **Laravel**: `admin/storage/logs/laravel.log`
- **Frontend**: Browser console

Details: [Setup Guide - Troubleshooting](docs/SETUP_GUIDE_JP.md#トラブルシューティング)

## ✅ Development Status

### Core Features
- ✅ **Backend API** (Flask) - Fully implemented
- ✅ **Frontend UI** (Next.js) - Fully implemented
- ✅ **XRPL Integration** - NFT minting, wallet management
- ✅ **Database Design** - Complete schema and migrations
- ✅ **Authentication System** - Google OAuth + JWT
- ✅ **Payment System** - Stripe integration

### Advanced Features
- ✅ **Referral System** - Coin rewards, exclusive product access
- ✅ **Escrow Staking** - XRP locking, NFT rewards
- ✅ **User Importance** - Score calculation, level management
- ✅ **Batch Transfer** - Bulk XRP distribution with XRPL Tickets
- ✅ **Analytics** - DAU/MAU/engagement analysis

### Management Features
- ✅ **Admin Panel** - Full-featured Laravel admin interface
- ✅ **Dashboard** - Real-time statistics display
- ✅ **Referral Management** - Rankings, detailed history
- ✅ **User Management** - Importance scores, VIP management
- ✅ **Batch Transfer Management** - Monitor and execute bulk transfers

### Infrastructure
- ✅ **Deployment Configuration** - Production-ready
- ✅ **Security** - JWT authentication, CORS configuration
- ✅ **Logging** - Comprehensive logging system
- ✅ **Error Handling** - Unified error processing

## License

Proprietary - Airzone Project

## Support

If you encounter issues, please check:

- [Troubleshooting](docs/SETUP_GUIDE_JP.md#トラブルシューティング)
- Log files: `backend/logs/app.log`
- Laravel logs: `admin/storage/logs/laravel.log`

## Reference Links

- [XRPL Official Documentation](https://xrpl.org/)
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Next.js Official Documentation](https://nextjs.org/docs)
- [Laravel Official Documentation](https://laravel.com/docs/10.x)
- [Xaman Wallet](https://xaman.app/)

## PV & Pitch & Website

- **PV**: https://youtu.be/atGWUDFrQtA  
- **Pitch Deck**: https://www.canva.com/design/DAG4wX75q2Q/8x4YbLt6gLt0rS4JGVMSMA/view
- **Website**: https://airz.one/

## Target Prize

- XRPL Main Track
- XRPL Deep Track
