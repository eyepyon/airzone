# Airzone NFT Smart Contract Deployment Guide

This guide walks you through deploying the Airzone NFT smart contract to the Sui blockchain.

## Prerequisites

### 1. Install Sui CLI

Install the Sui CLI tool:

```bash
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch testnet sui
```

Verify installation:

```bash
sui --version
```

### 2. Configure Sui Wallet

Initialize your Sui wallet:

```bash
sui client
```

This will create a new wallet and configuration. Follow the prompts to:
- Create a new wallet or import an existing one
- Select the network (testnet recommended for development)

Check your active address:

```bash
sui client active-address
```

### 3. Fund Your Wallet

For testnet/devnet, get test tokens from the faucet:

```bash
sui client faucet
```

Or use curl:

```bash
curl --location --request POST 'https://faucet.testnet.sui.io/gas' \
  --header 'Content-Type: application/json' \
  --data-raw '{"FixedAmountRequest":{"recipient":"YOUR_ADDRESS"}}'
```

Check your balance:

```bash
sui client gas
```

## Deployment Steps

### Step 1: Generate Sponsor Wallet

The sponsor wallet pays gas fees for NFT minting transactions:

```bash
cd scripts
python generate_sponsor_wallet.py
```

Follow the prompts to:
1. Select network (testnet/devnet/mainnet)
2. Save the generated wallet details
3. Fund the sponsor wallet using the provided instructions

**Important:** Keep the sponsor private key secure and add it to `backend/.env`:

```env
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=your-generated-private-key
```

### Step 2: Build the Contract

Navigate to the contracts directory and build:

```bash
cd contracts
sui move build
```

This will compile the Move code and check for errors.

### Step 3: Deploy to Sui Network

Use the deployment script:

```bash
# Deploy to testnet (default)
bash scripts/deploy_contract.sh testnet

# Or deploy to devnet
bash scripts/deploy_contract.sh devnet

# Or deploy to mainnet (production)
bash scripts/deploy_contract.sh mainnet
```

The script will:
1. Check prerequisites (Sui CLI, wallet, balance)
2. Build the contract
3. Deploy to the specified network
4. Extract the package ID
5. Update `backend/.env` with the package ID

### Step 4: Verify Deployment

After deployment, you'll see output like:

```
==========================================
Deployment Summary
==========================================

Network:            testnet
Package ID:         0x1234567890abcdef...
Transaction Digest: ABC123...
Deployer Address:   0xYourAddress...
```

The package ID is automatically added to `backend/.env`:

```env
SUI_PACKAGE_ID=0x1234567890abcdef...
```

### Step 5: View on Sui Explorer

Visit the Sui Explorer to view your deployed contract:

- **Testnet:** https://suiexplorer.com/object/YOUR_PACKAGE_ID?network=testnet
- **Devnet:** https://suiexplorer.com/object/YOUR_PACKAGE_ID?network=devnet
- **Mainnet:** https://suiexplorer.com/object/YOUR_PACKAGE_ID

### Step 6: Test NFT Minting

Test the NFT minting functionality:

```bash
cd backend
python verify_sui_client.py
```

This will:
1. Initialize the Sui client with your configuration
2. Generate a test wallet
3. Attempt to mint an NFT using sponsored transactions
4. Verify the NFT was created

## Configuration Summary

After deployment, your `backend/.env` should contain:

```env
# Sui Blockchain Configuration
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey1...
SUI_PACKAGE_ID=0x1234567890abcdef...
```

## Troubleshooting

### Build Errors

If you encounter build errors:

1. Check Move.toml dependencies are correct
2. Ensure Sui CLI is up to date
3. Review error messages for syntax issues

### Deployment Fails

If deployment fails:

1. **Insufficient balance:** Fund your wallet with more SUI
2. **Gas budget too low:** Increase gas budget in deploy script
3. **Network issues:** Check your internet connection and try again

### Package ID Not Found

If the package ID isn't extracted:

1. Check the deployment output manually
2. Look for `"type": "published"` in the JSON output
3. Extract the `packageId` field manually

### Sponsor Wallet Issues

If sponsored transactions fail:

1. Verify sponsor wallet has sufficient balance
2. Check sponsor private key is correct in .env
3. Ensure sponsor wallet is on the same network as deployment

## Upgrading the Contract

To upgrade the contract after changes:

1. Make changes to `contracts/sources/airzone_nft.move`
2. Build: `sui move build`
3. Deploy again: `bash scripts/deploy_contract.sh`
4. Update the package ID in `backend/.env`

**Note:** Sui uses an immutable package model. Each deployment creates a new package. You'll need to update the package ID in your configuration after each deployment.

## Security Considerations

### Sponsor Wallet Security

- **Never commit** the sponsor private key to version control
- Store the private key securely (use environment variables or secrets management)
- Monitor sponsor wallet balance regularly
- Set up alerts for low balance
- Use separate sponsor wallets for different environments (dev/staging/prod)

### Contract Security

- Audit the Move code before mainnet deployment
- Test thoroughly on testnet before deploying to mainnet
- Consider using a multi-sig wallet for mainnet deployments
- Monitor contract usage and transactions

### Access Control

- Only authorized addresses should be able to call admin functions
- Implement rate limiting on the backend to prevent abuse
- Monitor for unusual minting patterns

## Production Deployment Checklist

Before deploying to mainnet:

- [ ] Contract code reviewed and audited
- [ ] Thoroughly tested on testnet
- [ ] Sponsor wallet funded with sufficient SUI (recommend 100+ SUI)
- [ ] Backup of sponsor wallet private key stored securely
- [ ] Monitoring and alerting set up
- [ ] Rate limiting configured on backend
- [ ] Error handling tested
- [ ] Rollback plan prepared

## Support

For issues or questions:

1. Check the Sui documentation: https://docs.sui.io/
2. Review the Move language guide: https://move-language.github.io/move/
3. Join the Sui Discord: https://discord.gg/sui

## Requirements Mapping

This deployment process satisfies:

- **Requirement 3.2:** NFT minting via Move smart contract
- **Requirement 3.3:** Sponsored transactions (sponsor pays gas fees)
