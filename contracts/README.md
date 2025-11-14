# Airzone NFT Smart Contract

This directory contains the Sui Move smart contract for the Airzone NFT system.

## Overview

The Airzone NFT contract implements a WiFi-triggered NFT distribution system on the Sui blockchain. Users receive NFTs automatically when they connect to WiFi and authenticate through the captive portal.

## Features

- **NFT Minting**: Create unique NFTs with metadata (name, description, image URL)
- **Sponsored Transactions**: System sponsor wallet pays gas fees for users
- **NFT Transfer**: Transfer NFTs between wallets
- **Metadata Management**: Store and retrieve NFT metadata on-chain

## Project Structure

```
contracts/
├── Move.toml              # Package configuration
├── sources/
│   └── airzone_nft.move  # Main NFT module
└── README.md             # This file
```

## Prerequisites

- Sui CLI installed (`cargo install --locked --git https://github.com/MystenLabs/sui.git --branch testnet sui`)
- Sui wallet configured for testnet

## Building

```bash
cd contracts
sui move build
```

## Testing

```bash
cd contracts
sui move test
```

## Deployment

### Quick Start

For a quick deployment guide, see [QUICK_DEPLOY.md](./QUICK_DEPLOY.md).

### Automated Deployment

Use the deployment script for automated deployment:

```bash
# Deploy to testnet (recommended for development)
bash scripts/deploy_contract.sh testnet

# Deploy to devnet
bash scripts/deploy_contract.sh devnet

# Deploy to mainnet (production only)
bash scripts/deploy_contract.sh mainnet
```

The script will:
1. Check prerequisites (Sui CLI, wallet, balance)
2. Build the contract
3. Deploy to the specified network
4. Extract and save the package ID
5. Automatically update `backend/.env` with the package ID

### Manual Deployment

If you prefer manual deployment:

```bash
cd contracts
sui move build
sui client publish --gas-budget 100000000
```

After deployment, manually update `backend/.env` with:
- `SUI_PACKAGE_ID`: The published package ID
- `SUI_SPONSOR_PRIVATE_KEY`: The sponsor wallet private key

### Deployment Documentation

- **Quick Guide**: [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) - 5-step quick start
- **Full Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md) - Complete deployment documentation
- **Status**: [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md) - Current deployment status and checklist

### Verify Deployment

After deployment, verify the contract is working:

```bash
cd backend
python ../scripts/verify_contract.py
```

This will test NFT minting with sponsored transactions.

## Contract Interface

### Structures

- `AirzoneNFT`: Main NFT object with metadata fields

### Functions

- `mint(name, description, image_url, recipient, ctx)`: Mint a new NFT
- `transfer(nft, recipient)`: Transfer NFT to another address
- `update_metadata(nft, name, description, image_url, ctx)`: Update NFT metadata (owner only)
- `burn(nft)`: Burn/destroy an NFT (owner only)

## Requirements Mapping

- **Requirement 3.2**: NFT minting via Move smart contract
- **Requirement 3.3**: Sponsored transactions (sponsor pays gas fees)

## Security Considerations

- Only the NFT owner can transfer or burn their NFT
- Only the NFT owner can update metadata
- Sponsor wallet must be kept secure as it pays for all minting transactions
- All transactions are immutable on the blockchain

## License

Proprietary - Airzone Project
