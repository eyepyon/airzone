# Deployment Checklist

Quick checklist for deploying the Airzone NFT smart contract.

## Pre-Deployment

- [ ] Sui CLI installed (`sui --version`)
- [ ] Sui wallet configured (`sui client active-address`)
- [ ] Deployer wallet funded (≥0.1 SUI) (`sui client gas`)
- [ ] Sponsor wallet generated (`python scripts/generate_sponsor_wallet.py`)
- [ ] Sponsor wallet funded (≥1 SUI recommended)
- [ ] `backend/.env` file created from `.env.example`
- [ ] `SUI_NETWORK` set in .env (testnet/devnet/mainnet)
- [ ] `SUI_SPONSOR_PRIVATE_KEY` set in .env

## Deployment

- [ ] Run: `bash scripts/deploy_contract.sh testnet`
- [ ] Verify deployment output shows success
- [ ] Confirm package ID displayed
- [ ] Check `backend/.env` updated with `SUI_PACKAGE_ID`

## Post-Deployment

- [ ] Run: `python scripts/verify_contract.py`
- [ ] Verify NFT minting test passes
- [ ] Check contract on Sui Explorer
- [ ] Test backend NFT service integration
- [ ] Document package ID for team

## Quick Commands

```bash
# Check prerequisites
sui --version
sui client active-address
sui client gas

# Generate sponsor wallet
cd scripts && python generate_sponsor_wallet.py

# Deploy contract
bash scripts/deploy_contract.sh testnet

# Verify deployment
cd backend && python ../scripts/verify_contract.py
```

## Configuration Check

After deployment, `backend/.env` should have:

```env
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey1...
SUI_PACKAGE_ID=0x...
```

## Success Criteria

✅ Deployment script completes without errors  
✅ Package ID extracted and saved to .env  
✅ Verification script confirms NFT minting works  
✅ Contract visible on Sui Explorer  
✅ Sponsored transactions functioning  

## If Something Goes Wrong

1. Check error message carefully
2. Verify all prerequisites are met
3. Consult [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting
4. Check [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md) for common issues

## Support

- Full guide: [DEPLOYMENT.md](./DEPLOYMENT.md)
- Quick guide: [QUICK_DEPLOY.md](./QUICK_DEPLOY.md)
- Status: [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md)
- Sui docs: https://docs.sui.io/
