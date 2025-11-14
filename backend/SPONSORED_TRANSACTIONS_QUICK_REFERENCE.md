# Sponsored Transactions - Quick Reference

## Quick Start (5 Minutes)

### 1. Generate Sponsor Wallet
```bash
python scripts/generate_sponsor_wallet.py
```

### 2. Fund Sponsor Wallet (Testnet)
```bash
# Copy sponsor address from step 1, then:
curl --location --request POST 'https://faucet.testnet.sui.io/gas' \
  --header 'Content-Type: application/json' \
  --data-raw '{"FixedAmountRequest":{"recipient":"YOUR_SPONSOR_ADDRESS"}}'
```

### 3. Configure Environment
Add to `backend/.env`:
```bash
SUI_NETWORK=testnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey...
SUI_PACKAGE_ID=0x...  # After contract deployment
```

### 4. Verify Setup
```bash
python backend/verify_sponsored_transactions.py
```

## Common Operations

### Check Sponsor Balance
```python
from clients.sui_client import SuiClient
from config import Config

client = SuiClient(
    network=Config.SUI_NETWORK,
    sponsor_private_key=Config.SUI_SPONSOR_PRIVATE_KEY
)

balance = client.get_sponsor_balance()
print(f"Balance: {balance / 1_000_000_000:.4f} SUI")
```

### Check Sponsor Health
```python
health = client.check_sponsor_health()
print(f"Healthy: {health['healthy']}")
print(f"Balance: {health['balance_sui']:.4f} SUI")
print(f"Remaining TXs: {health['estimated_remaining_transactions']}")

for warning in health.get('warnings', []):
    print(f"⚠️  {warning}")
```

### Mint NFT with Sponsored Transaction
```python
result = client.mint_nft(
    recipient_address='0x...',
    nft_name='Welcome NFT',
    nft_description='Thank you for connecting',
    nft_image_url='https://example.com/nft.png',
    use_sponsor=True
)

print(f"✓ NFT: {result['nft_object_id']}")
print(f"  TX: {result['transaction_digest']}")
print(f"  Gas: {result['gas_used'] / 1_000_000_000:.6f} SUI")
```

## API Reference

### Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `get_sponsor_balance()` | Get sponsor wallet balance | `int` (MIST) |
| `validate_sponsor_balance(required)` | Check if balance is sufficient | `bool` |
| `estimate_gas_cost()` | Estimate gas for NFT mint | `int` (MIST) |
| `check_sponsor_health()` | Comprehensive health check | `Dict` |
| `mint_nft(..., use_sponsor=True)` | Mint NFT with sponsor | `Dict` |

### Balance Thresholds

| Level | Amount | Status | Action |
|-------|--------|--------|--------|
| Critical | < 0.05 SUI | ❌ | Fund immediately |
| Warning | < 0.5 SUI | ⚠️ | Fund soon |
| Healthy | ≥ 1 SUI | ✅ | Normal operation |

## Troubleshooting

### "Sponsor keypair not configured"
```bash
python scripts/generate_sponsor_wallet.py
# Add SUI_SPONSOR_PRIVATE_KEY to .env
```

### "Insufficient sponsor wallet balance"
```bash
# Testnet
curl --location --request POST 'https://faucet.testnet.sui.io/gas' \
  --header 'Content-Type: application/json' \
  --data-raw '{"FixedAmountRequest":{"recipient":"YOUR_ADDRESS"}}'
```

### "Package ID not configured"
```bash
bash scripts/deploy_contract.sh testnet
# Add SUI_PACKAGE_ID to .env
```

## Monitoring Commands

### Check Balance
```bash
python -c "from clients.sui_client import SuiClient; from config import Config; c = SuiClient(Config.SUI_NETWORK, Config.SUI_SPONSOR_PRIVATE_KEY); print(f'{c.get_sponsor_balance() / 1e9:.4f} SUI')"
```

### Health Check
```bash
python backend/verify_sponsored_transactions.py
```

### Estimate Remaining Transactions
```bash
python -c "from clients.sui_client import SuiClient; from config import Config; c = SuiClient(Config.SUI_NETWORK, Config.SUI_SPONSOR_PRIVATE_KEY); b = c.get_sponsor_balance(); g = c.estimate_gas_cost(); print(f'{b // g} transactions remaining')"
```

## Environment Variables

```bash
# Required
SUI_NETWORK=testnet                    # testnet, devnet, or mainnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey...  # From generate_sponsor_wallet.py
SUI_PACKAGE_ID=0x...                   # From deploy_contract.sh

# Optional (defaults shown)
JWT_SECRET_KEY=...                     # For API authentication
DB_HOST=localhost                      # Database host
```

## Gas Costs

| Operation | Typical Cost | Budget |
|-----------|--------------|--------|
| NFT Mint | 0.01-0.05 SUI | 0.1 SUI |
| NFT Transfer | 0.005-0.02 SUI | 0.05 SUI |

## Funding Strategy

### Testnet/Devnet
- Use faucet for free tokens
- Maintain 2-5 SUI
- Refill when < 0.5 SUI

### Mainnet
- Maintain minimum 10 SUI
- Set up alerts at 5 SUI
- Plan for 100-1000 TXs per funding

## Security Checklist

- [ ] Sponsor private key in `.env` (not in code)
- [ ] `.env` in `.gitignore`
- [ ] Different sponsor wallets for test/prod
- [ ] Balance monitoring enabled
- [ ] Low-balance alerts configured
- [ ] Regular key rotation scheduled

## Links

- **Full Documentation:** `backend/SPONSORED_TRANSACTIONS.md`
- **Implementation:** `backend/clients/sui_client.py`
- **Verification:** `backend/verify_sponsored_transactions.py`
- **Smart Contract:** `contracts/sources/airzone_nft.move`

---

**Need Help?** See `backend/SPONSORED_TRANSACTIONS.md` for detailed documentation.
