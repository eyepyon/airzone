# Airzone NFT - Quick Start Guide

Get the Airzone NFT smart contract up and running in minutes.

## Prerequisites

- Sui CLI installed
- Python 3.11+
- Backend environment configured

## 5-Minute Setup

### 1. Install Sui CLI (if not installed)

```bash
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch testnet sui
```

### 2. Generate Sponsor Wallet

```bash
cd scripts
python generate_sponsor_wallet.py
```

- Select network (1 for testnet)
- Save the output
- Copy the configuration to `backend/.env`

### 3. Fund Sponsor Wallet

Get testnet tokens:

```bash
sui client faucet --address YOUR_SPONSOR_ADDRESS
```

Or use the curl command from the wallet generator output.

### 4. Deploy Contract

```bash
bash scripts/deploy_contract.sh testnet
```

The script will:
- Build the contract
- Deploy to testnet
- Update `backend/.env` with package ID

### 5. Verify Deployment

```bash
python scripts/verify_contract.py
```

This tests the complete flow including minting a test NFT.

## Configuration Check

Your `backend/.env` should now have:

```env
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey1...
SUI_PACKAGE_ID=0x...
```

## Test NFT Minting

From your backend:

```python
from clients.sui_client import SuiClient

client = SuiClient(
    network='testnet',
    sponsor_private_key='your-sponsor-key',
    package_id='your-package-id'
)

result = client.mint_nft(
    recipient_address='0x...',
    nft_name='My First NFT',
    nft_description='Testing Airzone NFT',
    nft_image_url='https://example.com/nft.png',
    use_sponsor=True
)

print(f"NFT minted: {result['nft_object_id']}")
```

## Common Commands

### Build Contract
```bash
cd contracts
sui move build
```

### Run Tests
```bash
cd contracts
sui move test
```

### Check Sponsor Balance
```bash
sui client gas --address YOUR_SPONSOR_ADDRESS
```

### View on Explorer
```
https://suiexplorer.com/object/YOUR_PACKAGE_ID?network=testnet
```

## Troubleshooting

### "Sui CLI not found"
Install Sui CLI (see step 1)

### "Insufficient balance"
Fund your sponsor wallet with testnet tokens

### "Package ID not configured"
Run the deployment script

### "Transaction failed"
- Check sponsor wallet balance
- Verify network configuration
- Review error logs

## Next Steps

1. ✅ Contract deployed
2. ✅ Sponsor wallet funded
3. ✅ Configuration complete
4. → Integrate with your application
5. → Test end-to-end user flow
6. → Monitor and optimize

## Need Help?

- Read `DEPLOYMENT.md` for detailed instructions
- Check `IMPLEMENTATION_SUMMARY.md` for architecture details
- Review `README.md` for project overview
- Run `python scripts/verify_contract.py` for diagnostics

## Production Deployment

When ready for mainnet:

1. Generate new sponsor wallet for mainnet
2. Fund with real SUI tokens (recommend 100+ SUI)
3. Deploy: `bash scripts/deploy_contract.sh mainnet`
4. Update `.env` with mainnet configuration
5. Test thoroughly before going live

---

**Ready to mint NFTs!** 🎉

The contract is deployed and your application can now mint NFTs with sponsored transactions.
