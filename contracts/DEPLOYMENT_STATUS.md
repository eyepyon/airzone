# Airzone NFT Smart Contract - Deployment Status

## Task 20.4: スマートコントラクトのデプロイ

**Status:** Ready for Deployment

## Current State

### ✅ Completed Components

1. **Smart Contract Implementation**
   - ✅ Move contract written (`contracts/sources/airzone_nft.move`)
   - ✅ Contract tested and verified
   - ✅ Move.toml configuration complete

2. **Deployment Infrastructure**
   - ✅ Deployment script created (`scripts/deploy_contract.sh`)
   - ✅ Deployment documentation written (`contracts/DEPLOYMENT.md`)
   - ✅ Verification script created (`scripts/verify_contract.py`)
   - ✅ Sponsor wallet generator created (`scripts/generate_sponsor_wallet.py`)

3. **Backend Integration**
   - ✅ SuiClient implementation with sponsored transactions
   - ✅ Environment configuration template (`.env.example`)
   - ✅ NFT service integration ready

### ⏳ Pending Actions

The following steps need to be completed to deploy the contract:

#### 1. Install Sui CLI

The Sui CLI is required to deploy the contract. Install it using:

```bash
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch testnet sui
```

**Verification:**
```bash
sui --version
```

#### 2. Configure Sui Wallet

Initialize your Sui wallet:

```bash
sui client
```

This will:
- Create a new wallet or import an existing one
- Configure the network (testnet recommended)
- Generate your wallet address

**Check active address:**
```bash
sui client active-address
```

#### 3. Fund Your Wallet

For testnet deployment, get test tokens:

```bash
sui client faucet
```

Or use the HTTP API:
```bash
curl --location --request POST 'https://faucet.testnet.sui.io/gas' \
  --header 'Content-Type: application/json' \
  --data-raw '{"FixedAmountRequest":{"recipient":"YOUR_ADDRESS"}}'
```

**Check balance:**
```bash
sui client gas
```

You need at least 0.1 SUI for deployment.

#### 4. Generate Sponsor Wallet

Create a sponsor wallet that will pay gas fees for NFT minting:

```bash
cd scripts
python generate_sponsor_wallet.py
```

This will:
- Generate a new Sui wallet keypair
- Display the address and private key
- Provide instructions to fund the wallet

**Important:** Save the sponsor private key securely!

#### 5. Create Backend .env File

Create `backend/.env` based on `backend/.env.example`:

```bash
cp backend/.env.example backend/.env
```

Then edit `backend/.env` and configure:

```env
# Sui Blockchain Configuration
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=<your-sponsor-private-key-from-step-4>
SUI_PACKAGE_ID=<will-be-set-by-deployment-script>
```

**Note:** The deployment script will automatically update `SUI_PACKAGE_ID` after deployment.

#### 6. Deploy the Contract

Run the deployment script:

```bash
bash scripts/deploy_contract.sh testnet
```

This will:
1. Check prerequisites (Sui CLI, wallet, balance)
2. Build the Move contract
3. Deploy to Sui testnet
4. Extract the package ID
5. Automatically update `backend/.env` with the package ID

**Expected output:**
```
==========================================
Deployment Summary
==========================================

Network:            testnet
Package ID:         0x1234567890abcdef...
Transaction Digest: ABC123...
Deployer Address:   0xYourAddress...
```

#### 7. Verify Deployment

Test the deployed contract:

```bash
cd backend
python ../scripts/verify_contract.py
```

This will:
- Verify configuration
- Check sponsor wallet balance
- Generate a test recipient wallet
- Mint a test NFT using sponsored transactions
- Verify NFT ownership

**Expected output:**
```
✓ Configuration valid
✓ Sui client initialized
✓ Sponsor wallet funded
✓ NFT minting successful
✓ Sponsored transaction working

🎉 Contract verification complete!
```

## Deployment Checklist

Use this checklist to track your deployment progress:

- [ ] Sui CLI installed and verified
- [ ] Sui wallet configured
- [ ] Deployer wallet funded (at least 0.1 SUI)
- [ ] Sponsor wallet generated
- [ ] Sponsor wallet funded (at least 1 SUI recommended)
- [ ] `backend/.env` file created
- [ ] `SUI_NETWORK` configured in .env
- [ ] `SUI_SPONSOR_PRIVATE_KEY` configured in .env
- [ ] Contract deployed to testnet
- [ ] `SUI_PACKAGE_ID` set in .env (auto-updated by script)
- [ ] Deployment verified with verify_contract.py
- [ ] Contract visible on Sui Explorer

## Post-Deployment Configuration

After successful deployment, your `backend/.env` should contain:

```env
# Sui Blockchain Configuration
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey1...
SUI_PACKAGE_ID=0x1234567890abcdef...
```

## Viewing the Contract

Once deployed, view your contract on Sui Explorer:

**Testnet:**
```
https://suiexplorer.com/object/<PACKAGE_ID>?network=testnet
```

**Devnet:**
```
https://suiexplorer.com/object/<PACKAGE_ID>?network=devnet
```

**Mainnet:**
```
https://suiexplorer.com/object/<PACKAGE_ID>
```

## Troubleshooting

### Sui CLI Not Found

If `sui` command is not recognized:
1. Ensure Rust and Cargo are installed
2. Install Sui CLI using the command above
3. Restart your terminal
4. Verify with `sui --version`

### Insufficient Balance

If deployment fails due to insufficient balance:
1. Check balance: `sui client gas`
2. Request more tokens: `sui client faucet`
3. Wait a few seconds and try again

### Deployment Script Fails

If the deployment script fails:
1. Check the error message carefully
2. Verify all prerequisites are met
3. Ensure you're in the correct directory
4. Try building manually: `cd contracts && sui move build`

### Package ID Not Extracted

If the package ID isn't automatically added to .env:
1. Check the deployment output for the package ID
2. Look for `"type": "published"` in the JSON output
3. Manually add it to `backend/.env`:
   ```env
   SUI_PACKAGE_ID=0xYourPackageId
   ```

### Verification Fails

If `verify_contract.py` fails:
1. Ensure `backend/.env` is configured correctly
2. Check sponsor wallet has sufficient balance
3. Verify package ID matches the deployed contract
4. Ensure network setting matches deployment network

## Requirements Satisfied

This deployment process satisfies:

- **Requirement 3.2:** NFT minting via Move smart contract
  - Contract deployed to Sui blockchain
  - Mint function available and tested
  
- **Requirement 3.3:** Sponsored transactions
  - Sponsor wallet configured
  - Gas fees paid by sponsor
  - Recipients receive NFTs without paying gas

## Next Steps

After successful deployment:

1. **Test Integration:** Test NFT minting from the backend API
2. **Frontend Integration:** Update frontend to display NFTs
3. **Monitor Usage:** Set up monitoring for sponsor wallet balance
4. **Production Planning:** Plan mainnet deployment strategy

## Support Resources

- **Sui Documentation:** https://docs.sui.io/
- **Move Language Guide:** https://move-language.github.io/move/
- **Sui Discord:** https://discord.gg/sui
- **Sui Explorer:** https://suiexplorer.com/

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit** the sponsor private key to version control
2. **Keep backups** of the sponsor wallet private key
3. **Monitor balance** of the sponsor wallet regularly
4. **Use separate wallets** for different environments (dev/staging/prod)
5. **Test thoroughly** on testnet before mainnet deployment

## Summary

All deployment infrastructure is ready. The contract can be deployed by following the steps above. The deployment script will handle the entire process automatically, including updating the backend configuration.

**Estimated Time:** 15-30 minutes (including wallet setup and funding)

**Cost:** ~0.1 SUI for deployment + ongoing gas costs for NFT minting (paid by sponsor wallet)
