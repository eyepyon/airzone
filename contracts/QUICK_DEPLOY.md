# Quick Deployment Guide

## Prerequisites Check

```bash
# 1. Check if Sui CLI is installed
sui --version

# 2. Check if wallet is configured
sui client active-address

# 3. Check wallet balance
sui client gas
```

## Quick Deploy (5 Steps)

### Step 1: Install Sui CLI (if needed)

```bash
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch testnet sui
```

### Step 2: Setup Wallet & Get Testnet Tokens

```bash
# Initialize wallet
sui client

# Get testnet tokens
sui client faucet
```

### Step 3: Generate Sponsor Wallet

```bash
cd scripts
python generate_sponsor_wallet.py
```

Save the private key output!

### Step 4: Configure Environment

```bash
# Create .env file
cp backend/.env.example backend/.env

# Edit backend/.env and add:
# SUI_NETWORK=testnet
# SUI_SPONSOR_PRIVATE_KEY=<from-step-3>
```

### Step 5: Deploy Contract

```bash
# Deploy to testnet
bash scripts/deploy_contract.sh testnet
```

The script will automatically update `backend/.env` with the package ID.

## Verify Deployment

```bash
cd backend
python ../scripts/verify_contract.py
```

## View on Explorer

After deployment, visit:
```
https://suiexplorer.com/object/<PACKAGE_ID>?network=testnet
```

## Troubleshooting

**Sui CLI not found?**
- Install Rust: https://rustup.rs/
- Install Sui CLI (see Step 1)
- Restart terminal

**Insufficient balance?**
- Run: `sui client faucet`
- Wait 30 seconds and try again

**Deployment fails?**
- Check balance: `sui client gas`
- Verify you're in project root directory
- Check error message in output

## What Gets Configured

After successful deployment, `backend/.env` will have:

```env
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey1...
SUI_PACKAGE_ID=0x...  # Auto-updated by deploy script
```

## Next Steps

1. ✅ Contract deployed
2. ✅ Configuration updated
3. ➡️ Test with: `python scripts/verify_contract.py`
4. ➡️ Integrate with backend API
5. ➡️ Test NFT minting from application

## Need Help?

- Full guide: See `DEPLOYMENT.md`
- Status: See `DEPLOYMENT_STATUS.md`
- Sui docs: https://docs.sui.io/
