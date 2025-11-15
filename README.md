# Airzone

WiFi-triggered NFT distribution and EC shop platform powered by Sui blockchain.

## Overview

Airzone is a platform that automatically distributes NFTs to users when they connect to WiFi through a captive portal, and allows them to use those NFTs to purchase products in an integrated e-commerce shop.

## Project Structure

```
airzone/
├── backend/          # Flask API server
├── frontend/         # Next.js web application
├── contracts/        # Sui Move smart contracts
└── scripts/          # Deployment and utility scripts
```
  
メンバー開発リポジトリ  
https://github.com/Jun0908/sui-airzone  
  

## Quick Links

- **Backend Documentation:** [backend/README.md](backend/README.md)
- **Frontend Documentation:** [frontend/README.md](frontend/README.md)
- **Smart Contract Documentation:** [contracts/README.md](contracts/README.md)
- **Deployment Guide:** [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)

## Technology Stack

- **Backend:** Flask 3.0 + Python 3.11+ + SQLAlchemy
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- **Blockchain:** Sui (Move)
- **Database:** MySQL 8.0
- **Payment:** Stripe
- **Infrastructure:** Apache 2.4

## Getting Started

### 1. Database Setup

Set up the MySQL database first:

```bash
# Quick setup (recommended)
python scripts/setup_database.py

# Or use the platform-specific script
# Windows:
DATABASE_QUICK_SETUP.bat

# Linux/Mac:
bash DATABASE_QUICK_SETUP.sh
```

For detailed instructions, see [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)

### 2. Smart Contract Deployment

The smart contract is ready to deploy. See [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md) for instructions.

Quick start:
```bash
# Deploy to Sui testnet
bash scripts/deploy_contract.sh testnet

# Verify deployment
cd backend && python ../scripts/verify_contract.py
```

### 3. Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
pip install -r requirements.txt
python app.py
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Features

- **WiFi-Triggered NFT Distribution:** Automatic NFT minting when users connect to WiFi
- **Captive Portal Integration:** OpenNDS integration for seamless authentication
- **Sponsored Transactions:** System pays gas fees for NFT minting
- **NFT-Gated E-Commerce:** Products require specific NFTs to purchase
- **Stripe Payment Integration:** Secure payment processing
- **Google OAuth Authentication:** Easy user authentication

## Current Status

### ✅ Completed
- Backend API (Flask)
- Frontend UI (Next.js)
- Smart Contract (Sui Move)
- Database Setup & Migrations
- Deployment Infrastructure

### ⏳ Pending
- Apache configuration
- Production deployment

## Documentation

- **Database Setup:** [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)
- **Deployment:** [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)
- **Smart Contracts:** [contracts/README.md](contracts/README.md)
- **Backend API:** [backend/README.md](backend/README.md)
- **Frontend:** [frontend/README.md](frontend/README.md)
- **Specifications:** [.kiro/specs/airzone/](/.kiro/specs/airzone/)

## Requirements

- Node.js 18+
- Python 3.11+
- MySQL 8.0
- Sui CLI (for contract deployment)
- Apache 2.4 (for production)

## License

Proprietary - Airzone Project