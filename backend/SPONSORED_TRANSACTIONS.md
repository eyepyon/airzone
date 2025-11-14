# Sponsored Transactions Implementation

## Overview

This document describes the sponsored transaction implementation for the Airzone NFT system. Sponsored transactions allow the system to mint NFTs for users without requiring them to have SUI tokens or pay gas fees.

**Requirements:** 3.3 - Sponsored transactions (sponsor pays gas fees)

## How Sponsored Transactions Work

### Traditional Transaction Flow
```
User → Signs Transaction → Pays Gas Fee → Receives NFT
```

### Sponsored Transaction Flow
```
User → Authenticates → Backend → Sponsor Signs → Sponsor Pays Gas → User Receives NFT
```

## Key Features

### 1. Sponsor Wallet Management
- **Automatic Balance Checking**: Validates sponsor wallet has sufficient funds before transactions
- **Health Monitoring**: Tracks sponsor wallet balance and provides warnings
- **Gas Estimation**: Estimates gas costs for NFT minting operations
- **Balance Thresholds**: Defines critical, warning, and healthy balance levels

### 2. Transaction Execution
- **Sponsored Signing**: Sponsor wallet signs and pays for transactions
- **Recipient Transfer**: NFT is minted and transferred to recipient address
- **Gas Budget Management**: Sets appropriate gas budgets for transactions
- **Result Tracking**: Logs transaction details, gas used, and remaining balance

### 3. Error Handling
- **Balance Validation**: Prevents transactions if sponsor balance is too low
- **Configuration Checks**: Validates sponsor keypair and package ID
- **Detailed Logging**: Comprehensive logging of all transaction steps
- **Graceful Failures**: Clear error messages with actionable recommendations

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Backend Application                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              NFTService                               │  │
│  │  - Receives mint request                              │  │
│  │  - Queues background task                             │  │
│  └───────────────┬───────────────────────────────────────┘  │
│                  │                                           │
│  ┌───────────────▼───────────────────────────────────────┐  │
│  │              SuiClient                                │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  Sponsor Wallet Management                      │ │  │
│  │  │  - get_sponsor_balance()                        │ │  │
│  │  │  - validate_sponsor_balance()                   │ │  │
│  │  │  - check_sponsor_health()                       │ │  │
│  │  │  - estimate_gas_cost()                          │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  Sponsored Transaction Execution                │ │  │
│  │  │  - _execute_sponsored_transaction()             │ │  │
│  │  │  - Build Move call                              │ │  │
│  │  │  - Sign with sponsor keypair                    │ │  │
│  │  │  - Execute and track results                    │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └───────────────┬───────────────────────────────────────┘  │
└──────────────────┼───────────────────────────────────────────┘
                   │
                   │ RPC Call
                   │
┌──────────────────▼───────────────────────────────────────────┐
│                  Sui Blockchain Network                       │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Move Smart Contract: airzone_nft::nft::mint()        │  │
│  │  - Creates NFT object                                  │  │
│  │  - Transfers to recipient                              │  │
│  │  - Emits events                                        │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Implementation Details

### SuiClient Methods

#### `get_sponsor_balance() -> int`
Returns the current balance of the sponsor wallet in MIST.

```python
balance = client.get_sponsor_balance()
print(f"Balance: {balance / 1_000_000_000:.4f} SUI")
```

#### `validate_sponsor_balance(required_balance: int) -> bool`
Validates that the sponsor wallet has sufficient balance for transactions.

```python
if client.validate_sponsor_balance(required_balance=100_000_000):
    print("Sponsor wallet has sufficient balance")
else:
    print("Sponsor wallet needs funding")
```

#### `estimate_gas_cost() -> int`
Returns an estimated gas cost for NFT minting (conservative estimate).

```python
gas_cost = client.estimate_gas_cost()
print(f"Estimated gas: {gas_cost / 1_000_000_000:.6f} SUI")
```

#### `check_sponsor_health() -> Dict`
Comprehensive health check of the sponsor wallet.

```python
health = client.check_sponsor_health()
print(f"Healthy: {health['healthy']}")
print(f"Balance: {health['balance_sui']:.4f} SUI")
print(f"Estimated remaining transactions: {health['estimated_remaining_transactions']}")

for warning in health.get('warnings', []):
    print(f"Warning: {warning}")
```

#### `_execute_sponsored_transaction(...) -> Dict`
Internal method that executes the sponsored transaction.

**Process:**
1. Validates sponsor keypair is configured
2. Checks sponsor balance is sufficient
3. Builds Move call transaction
4. Signs with sponsor keypair
5. Executes transaction on blockchain
6. Parses results and extracts NFT object ID
7. Logs gas usage and remaining balance
8. Returns transaction details

### Configuration

Required environment variables in `backend/.env`:

```bash
# Sui Blockchain Configuration
SUI_NETWORK=testnet                    # Network: testnet, devnet, or mainnet
SUI_SPONSOR_PRIVATE_KEY=suiprivkey...  # Sponsor wallet private key
SUI_PACKAGE_ID=0x...                   # Deployed Move package ID
```

### Balance Thresholds

The system defines three balance thresholds:

| Threshold | Amount | Status | Action |
|-----------|--------|--------|--------|
| Critical | < 0.05 SUI | ❌ Unhealthy | Immediate funding required |
| Warning | < 0.5 SUI | ⚠️ Warning | Consider funding soon |
| Healthy | ≥ 1 SUI | ✅ Healthy | Normal operation |

### Gas Budget

- **Default Budget**: 0.1 SUI (100,000,000 MIST)
- **Typical Usage**: 0.01-0.05 SUI per NFT mint
- **Buffer**: Conservative estimate to ensure transaction success

## Usage Examples

### Basic NFT Minting with Sponsored Transaction

```python
from clients.sui_client import SuiClient

# Initialize client with sponsor
client = SuiClient(
    network='testnet',
    sponsor_private_key='suiprivkey...',
    package_id='0x...'
)

# Check sponsor health before minting
health = client.check_sponsor_health()
if not health['healthy']:
    print("Warning: Sponsor wallet needs attention")
    for warning in health['warnings']:
        print(f"  {warning}")

# Mint NFT with sponsored transaction
result = client.mint_nft(
    recipient_address='0x...',
    nft_name='Welcome NFT',
    nft_description='Thank you for connecting to our WiFi',
    nft_image_url='https://example.com/nft.png',
    use_sponsor=True  # Sponsor pays gas fees
)

print(f"NFT minted: {result['nft_object_id']}")
print(f"Transaction: {result['transaction_digest']}")
print(f"Gas used: {result['gas_used'] / 1_000_000_000:.6f} SUI")
print(f"Sponsor balance after: {result['sponsor_balance_after'] / 1_000_000_000:.4f} SUI")
```

### Monitoring Sponsor Wallet

```python
# Get current balance
balance = client.get_sponsor_balance()
balance_sui = balance / 1_000_000_000

print(f"Current balance: {balance_sui:.4f} SUI")

# Estimate remaining transactions
gas_per_tx = client.estimate_gas_cost()
remaining_txs = balance // gas_per_tx

print(f"Estimated remaining transactions: {remaining_txs}")

# Check if funding is needed
if balance < 500_000_000:  # Less than 0.5 SUI
    print("⚠️ Sponsor wallet should be funded soon")
```

### Health Check Integration

```python
def mint_with_health_check(client, recipient, nft_data):
    """Mint NFT with automatic health checking."""
    
    # Check sponsor health
    health = client.check_sponsor_health()
    
    if not health['healthy']:
        raise Exception(f"Sponsor wallet unhealthy: {health.get('error')}")
    
    # Warn if balance is low
    if health.get('warnings'):
        for warning in health['warnings']:
            logger.warning(f"Sponsor wallet: {warning}")
    
    # Proceed with minting
    return client.mint_nft(
        recipient_address=recipient,
        nft_name=nft_data['name'],
        nft_description=nft_data['description'],
        nft_image_url=nft_data['image_url'],
        use_sponsor=True
    )
```

## Testing

### Run Verification Script

```bash
# Test sponsored transaction implementation
python backend/verify_sponsored_transactions.py
```

The verification script tests:
- ✓ Sponsor wallet configuration
- ✓ Balance checking
- ✓ Balance validation
- ✓ Gas cost estimation
- ✓ Health monitoring
- ✓ Transaction preparation

### Manual Testing

```bash
# 1. Generate sponsor wallet
python scripts/generate_sponsor_wallet.py

# 2. Fund sponsor wallet (testnet)
curl --location --request POST 'https://faucet.testnet.sui.io/gas' \
  --header 'Content-Type: application/json' \
  --data-raw '{"FixedAmountRequest":{"recipient":"YOUR_SPONSOR_ADDRESS"}}'

# 3. Check sponsor health
python -c "
from clients.sui_client import SuiClient
from config import Config

client = SuiClient(
    network=Config.SUI_NETWORK,
    sponsor_private_key=Config.SUI_SPONSOR_PRIVATE_KEY
)

health = client.check_sponsor_health()
print(f'Healthy: {health[\"healthy\"]}')
print(f'Balance: {health[\"balance_sui\"]:.4f} SUI')
"

# 4. Deploy contract and test minting
bash scripts/deploy_contract.sh testnet
python backend/verify_sui_client.py
```

## Monitoring and Maintenance

### Daily Checks
- Monitor sponsor wallet balance
- Review transaction success rate
- Check gas usage trends

### Weekly Tasks
- Analyze gas cost patterns
- Review balance thresholds
- Update funding schedule

### Alerts to Set Up
- Critical: Balance < 0.05 SUI
- Warning: Balance < 0.5 SUI
- Info: Balance < 1 SUI

### Funding Strategy

**Testnet/Devnet:**
- Use faucet for free test tokens
- Refill when balance < 0.5 SUI
- Maintain 2-5 SUI for testing

**Mainnet:**
- Maintain minimum 10 SUI balance
- Set up automatic alerts
- Plan for 100-1000 transactions per funding
- Monitor gas price fluctuations

## Security Considerations

### Private Key Management
- ✅ Store sponsor private key in environment variables
- ✅ Never commit private keys to version control
- ✅ Use different sponsor wallets for different environments
- ✅ Rotate sponsor keys periodically

### Access Control
- ✅ Limit access to sponsor private key
- ✅ Use separate sponsor wallets for test/production
- ✅ Monitor sponsor wallet transactions
- ✅ Set up alerts for unusual activity

### Balance Management
- ✅ Maintain sufficient balance for operations
- ✅ Set up low-balance alerts
- ✅ Have backup funding plan
- ✅ Monitor gas price trends

## Troubleshooting

### "Sponsor keypair not configured"
**Solution:** Set `SUI_SPONSOR_PRIVATE_KEY` in `.env` file
```bash
python scripts/generate_sponsor_wallet.py
```

### "Insufficient sponsor wallet balance"
**Solution:** Fund the sponsor wallet
```bash
# Testnet
curl --location --request POST 'https://faucet.testnet.sui.io/gas' \
  --header 'Content-Type: application/json' \
  --data-raw '{"FixedAmountRequest":{"recipient":"YOUR_ADDRESS"}}'

# Mainnet
# Transfer SUI tokens to sponsor address
```

### "Package ID not configured"
**Solution:** Deploy the Move contract
```bash
bash scripts/deploy_contract.sh testnet
```

### "Transaction execution failed"
**Possible causes:**
- Insufficient sponsor balance
- Network connectivity issues
- Invalid Move contract call
- Gas budget too low

**Debug steps:**
1. Check sponsor balance: `python backend/verify_sponsored_transactions.py`
2. Verify network connectivity
3. Check contract deployment
4. Review transaction logs

## Performance Metrics

### Expected Performance
- **Transaction Time**: 2-5 seconds
- **Gas Cost**: 0.01-0.05 SUI per NFT
- **Success Rate**: > 99%
- **Concurrent Transactions**: Limited by sponsor wallet nonce

### Optimization Tips
- Batch transactions when possible
- Monitor gas prices and adjust budgets
- Use appropriate network (testnet for development)
- Implement retry logic for failed transactions

## Requirements Satisfied

✅ **Requirement 3.3: Sponsored Transactions**
- Sponsor wallet pays gas fees for NFT minting
- Recipients receive NFTs without needing SUI tokens
- Sponsor wallet configuration and management
- Balance validation and health monitoring
- Gas cost estimation and tracking
- Comprehensive error handling
- Transaction result tracking

## Related Documentation

- [Sui Client Implementation](./clients/sui_client.py)
- [NFT Service](./services/nft_service.py)
- [Smart Contract](../contracts/sources/airzone_nft.move)
- [Deployment Guide](../contracts/DEPLOYMENT.md)
- [Generate Sponsor Wallet](../scripts/generate_sponsor_wallet.py)

## API Reference

See [SuiClient API Documentation](./clients/sui_client.py) for detailed method signatures and parameters.

---

**Last Updated:** 2024
**Version:** 1.0
**Status:** ✅ Complete and Production Ready
