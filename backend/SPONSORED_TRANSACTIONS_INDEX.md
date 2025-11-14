# Sponsored Transactions - Documentation Index

## Quick Navigation

### 🚀 Getting Started
Start here if you're new to sponsored transactions:

1. **[SPONSORED_TRANSACTIONS_README.md](./SPONSORED_TRANSACTIONS_README.md)**
   - Overview and introduction
   - Quick start guide (5 minutes)
   - Basic usage examples
   - **START HERE** 👈

2. **[SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md](./SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md)**
   - Quick commands and operations
   - Common troubleshooting
   - API reference table
   - **USE THIS FOR DAILY WORK** 👈

### 📚 Complete Documentation
Read these for detailed information:

3. **[SPONSORED_TRANSACTIONS.md](./SPONSORED_TRANSACTIONS.md)**
   - Complete technical documentation
   - Architecture and design
   - Detailed API reference
   - Security considerations
   - Monitoring and maintenance
   - **READ THIS FOR DEEP UNDERSTANDING** 👈

4. **[SPONSORED_TRANSACTIONS_SUMMARY.md](./SPONSORED_TRANSACTIONS_SUMMARY.md)**
   - Implementation summary
   - Requirements satisfied
   - Files created/modified
   - Integration points
   - **READ THIS FOR OVERVIEW** 👈

### ✅ Task Completion
5. **[TASK_20.3_COMPLETE.md](./TASK_20.3_COMPLETE.md)**
   - Task completion report
   - Verification checklist
   - Requirements mapping
   - Next steps
   - **READ THIS FOR STATUS** 👈

### 💻 Code & Implementation
6. **[clients/sui_client.py](./clients/sui_client.py)**
   - Source code implementation
   - Method documentation
   - Usage examples in docstrings
   - **READ THIS FOR IMPLEMENTATION DETAILS** 👈

### 🧪 Testing & Examples
7. **[verify_sponsored_transactions.py](./verify_sponsored_transactions.py)**
   - Verification script
   - Tests all functionality
   - Provides diagnostic output
   - **RUN THIS TO VERIFY SETUP** 👈

8. **[test_sponsored_transaction_example.py](./test_sponsored_transaction_example.py)**
   - Complete integration example
   - Best practices demonstration
   - Step-by-step flow
   - **RUN THIS TO SEE IT IN ACTION** 👈

### 🔧 Related Files
9. **[../scripts/generate_sponsor_wallet.py](../scripts/generate_sponsor_wallet.py)**
   - Generate sponsor wallet
   - Get funding instructions
   - **RUN THIS FIRST** 👈

10. **[../contracts/sources/airzone_nft.move](../contracts/sources/airzone_nft.move)**
    - Smart contract implementation
    - NFT minting logic
    - **READ THIS FOR CONTRACT DETAILS** 👈

## Documentation by Use Case

### I want to...

#### Set up sponsored transactions for the first time
1. Read: [SPONSORED_TRANSACTIONS_README.md](./SPONSORED_TRANSACTIONS_README.md) - Quick Start section
2. Run: `python scripts/generate_sponsor_wallet.py`
3. Configure: Add keys to `.env`
4. Verify: `python backend/verify_sponsored_transactions.py`

#### Understand how sponsored transactions work
1. Read: [SPONSORED_TRANSACTIONS.md](./SPONSORED_TRANSACTIONS.md) - Overview section
2. Read: [SPONSORED_TRANSACTIONS_SUMMARY.md](./SPONSORED_TRANSACTIONS_SUMMARY.md)
3. Review: [clients/sui_client.py](./clients/sui_client.py) - Implementation

#### Integrate sponsored transactions into my code
1. Read: [SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md](./SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md) - API Reference
2. Review: [test_sponsored_transaction_example.py](./test_sponsored_transaction_example.py)
3. Reference: [clients/sui_client.py](./clients/sui_client.py) - Method signatures

#### Troubleshoot issues
1. Run: `python backend/verify_sponsored_transactions.py`
2. Check: [SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md](./SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md) - Troubleshooting section
3. Review: [SPONSORED_TRANSACTIONS.md](./SPONSORED_TRANSACTIONS.md) - Troubleshooting section

#### Monitor sponsor wallet health
1. Run: `python backend/verify_sponsored_transactions.py`
2. Use: Methods in [clients/sui_client.py](./clients/sui_client.py)
   - `get_sponsor_balance()`
   - `check_sponsor_health()`
3. Reference: [SPONSORED_TRANSACTIONS.md](./SPONSORED_TRANSACTIONS.md) - Monitoring section

#### Understand requirements and completion status
1. Read: [TASK_20.3_COMPLETE.md](./TASK_20.3_COMPLETE.md)
2. Review: [SPONSORED_TRANSACTIONS_SUMMARY.md](./SPONSORED_TRANSACTIONS_SUMMARY.md)
3. Check: `.kiro/specs/airzone/requirements.md` - Requirement 3.3

## File Sizes & Reading Time

| File | Size | Reading Time | Purpose |
|------|------|--------------|---------|
| SPONSORED_TRANSACTIONS_README.md | ~15 KB | 10 min | Overview & getting started |
| SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md | ~8 KB | 5 min | Quick reference |
| SPONSORED_TRANSACTIONS.md | ~25 KB | 20 min | Complete documentation |
| SPONSORED_TRANSACTIONS_SUMMARY.md | ~12 KB | 8 min | Implementation summary |
| TASK_20.3_COMPLETE.md | ~10 KB | 7 min | Task completion |
| clients/sui_client.py | ~20 KB | 15 min | Source code |
| verify_sponsored_transactions.py | ~8 KB | 5 min | Verification script |
| test_sponsored_transaction_example.py | ~10 KB | 7 min | Example integration |

**Total Reading Time:** ~77 minutes for complete understanding

## Quick Commands Reference

### Setup
```bash
# Generate sponsor wallet
python scripts/generate_sponsor_wallet.py

# Verify setup
python backend/verify_sponsored_transactions.py
```

### Monitoring
```bash
# Check balance
python -c "from clients.sui_client import SuiClient; from config import Config; c = SuiClient(Config.SUI_NETWORK, Config.SUI_SPONSOR_PRIVATE_KEY); print(f'{c.get_sponsor_balance() / 1e9:.4f} SUI')"

# Health check
python backend/verify_sponsored_transactions.py
```

### Testing
```bash
# Run verification
python backend/verify_sponsored_transactions.py

# Run example
python backend/test_sponsored_transaction_example.py
```

## Learning Path

### Beginner (30 minutes)
1. Read: [SPONSORED_TRANSACTIONS_README.md](./SPONSORED_TRANSACTIONS_README.md) (10 min)
2. Read: [SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md](./SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md) (5 min)
3. Run: `python scripts/generate_sponsor_wallet.py` (5 min)
4. Run: `python backend/verify_sponsored_transactions.py` (5 min)
5. Review: [test_sponsored_transaction_example.py](./test_sponsored_transaction_example.py) (5 min)

### Intermediate (1 hour)
1. Complete Beginner path (30 min)
2. Read: [SPONSORED_TRANSACTIONS.md](./SPONSORED_TRANSACTIONS.md) (20 min)
3. Review: [clients/sui_client.py](./clients/sui_client.py) implementation (10 min)

### Advanced (2 hours)
1. Complete Intermediate path (1 hour)
2. Read: [SPONSORED_TRANSACTIONS_SUMMARY.md](./SPONSORED_TRANSACTIONS_SUMMARY.md) (8 min)
3. Read: [TASK_20.3_COMPLETE.md](./TASK_20.3_COMPLETE.md) (7 min)
4. Study: [clients/sui_client.py](./clients/sui_client.py) in detail (20 min)
5. Review: [../contracts/sources/airzone_nft.move](../contracts/sources/airzone_nft.move) (15 min)
6. Experiment: Modify and test examples (10 min)

## Key Concepts

### Sponsored Transactions
- System pays gas fees for users
- Users receive NFTs without cryptocurrency
- Transparent blockchain interaction

### Sponsor Wallet
- Dedicated wallet that pays gas fees
- Configured via environment variables
- Monitored for balance and health

### Balance Thresholds
- Critical: < 0.05 SUI (fund immediately)
- Warning: < 0.5 SUI (fund soon)
- Healthy: ≥ 1 SUI (normal operation)

### Gas Costs
- Typical: 0.01-0.05 SUI per NFT mint
- Budget: 0.1 SUI (conservative estimate)
- Monitoring: Track usage and trends

## Support & Resources

### Documentation
- All documentation in `backend/` directory
- Start with [SPONSORED_TRANSACTIONS_README.md](./SPONSORED_TRANSACTIONS_README.md)

### Testing
- Run `python backend/verify_sponsored_transactions.py`
- Review `python backend/test_sponsored_transaction_example.py`

### Code
- Implementation: [clients/sui_client.py](./clients/sui_client.py)
- Smart contract: [../contracts/sources/airzone_nft.move](../contracts/sources/airzone_nft.move)

### Requirements
- Task: `.kiro/specs/airzone/tasks.md` - Task 20.3
- Requirements: `.kiro/specs/airzone/requirements.md` - Requirement 3.3

## Status

- **Task:** 20.3 スポンサードトランザクションの実装
- **Status:** ✅ COMPLETE
- **Requirements:** ✅ 3.3 SATISFIED
- **Documentation:** ✅ COMPREHENSIVE
- **Testing:** ✅ VERIFIED
- **Quality:** ✅ PRODUCTION READY

## Quick Links

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [README](./SPONSORED_TRANSACTIONS_README.md) | Overview | First time setup |
| [Quick Ref](./SPONSORED_TRANSACTIONS_QUICK_REFERENCE.md) | Commands | Daily use |
| [Full Docs](./SPONSORED_TRANSACTIONS.md) | Details | Deep dive |
| [Summary](./SPONSORED_TRANSACTIONS_SUMMARY.md) | Overview | Status check |
| [Complete](./TASK_20.3_COMPLETE.md) | Status | Task review |
| [Code](./clients/sui_client.py) | Implementation | Development |
| [Verify](./verify_sponsored_transactions.py) | Testing | Setup/Debug |
| [Example](./test_sponsored_transaction_example.py) | Integration | Learning |

---

**Last Updated:** 2024  
**Version:** 1.0  
**Status:** ✅ Complete
