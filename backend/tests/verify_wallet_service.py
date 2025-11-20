"""
Verification script for WalletService implementation.
Tests wallet creation, encryption, and retrieval functionality.

Requirements: 1.3, 6.2
"""
import sys
import os
from cryptography.fernet import Fernet

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.wallet import Wallet
from services.wallet_service import WalletService
from clients.xrpl_client import XRPLClient


def test_wallet_service():
    """Test WalletService functionality."""
    print("=" * 60)
    print("WalletService Verification")
    print("=" * 60)
    
    # Create in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    
    try:
        # Generate encryption key
        encryption_key = Fernet.generate_key()
        print(f"\n✓ Generated encryption key")
        
        # Initialize XRPLClient (testnet)
        xrpl_client = XRPLClient(network='testnet')
        print(f"✓ Initialized XRPLClient on testnet")
        
        # Initialize WalletService
        wallet_service = WalletService(
            db_session=db_session,
            xrpl_client=xrpl_client,
            encryption_key=encryption_key
        )
        print(f"✓ Initialized WalletService")
        
        # Create test user
        test_user = User(
            email='test@example.com',
            google_id='google_123',
            name='Test User'
        )
        db_session.add(test_user)
        db_session.commit()
        print(f"\n✓ Created test user: {test_user.id}")
        
        # Test 1: Create wallet
        print("\n" + "-" * 60)
        print("Test 1: Create Wallet")
        print("-" * 60)
        
        wallet_data = wallet_service.create_wallet(test_user.id)
        print(f"✓ Created wallet for user {test_user.id}")
        print(f"  - Wallet ID: {wallet_data['id']}")
        print(f"  - Address: {wallet_data['address']}")
        print(f"  - User ID: {wallet_data['user_id']}")
        
        # Verify private key is not in response
        assert 'private_key_encrypted' not in wallet_data, "Private key should not be in public response"
        print(f"✓ Private key correctly excluded from public response")
        
        # Test 2: Get user wallet
        print("\n" + "-" * 60)
        print("Test 2: Get User Wallet")
        print("-" * 60)
        
        retrieved_wallet = wallet_service.get_user_wallet(test_user.id)
        print(f"✓ Retrieved wallet for user {test_user.id}")
        assert retrieved_wallet['id'] == wallet_data['id'], "Wallet IDs should match"
        assert retrieved_wallet['address'] == wallet_data['address'], "Addresses should match"
        print(f"✓ Wallet data matches original")
        
        # Test 3: Get wallet by address
        print("\n" + "-" * 60)
        print("Test 3: Get Wallet by Address")
        print("-" * 60)
        
        wallet_by_address = wallet_service.get_wallet_by_address(wallet_data['address'])
        print(f"✓ Retrieved wallet by address: {wallet_data['address']}")
        assert wallet_by_address['id'] == wallet_data['id'], "Wallet IDs should match"
        print(f"✓ Wallet data matches original")
        
        # Test 4: Prevent duplicate wallet creation
        print("\n" + "-" * 60)
        print("Test 4: Prevent Duplicate Wallet Creation")
        print("-" * 60)
        
        duplicate_wallet = wallet_service.create_wallet(test_user.id)
        print(f"✓ Attempted to create duplicate wallet")
        assert duplicate_wallet['id'] == wallet_data['id'], "Should return existing wallet"
        print(f"✓ Correctly returned existing wallet instead of creating duplicate")
        
        # Test 5: Encryption/Decryption
        print("\n" + "-" * 60)
        print("Test 5: Private Key Encryption/Decryption")
        print("-" * 60)
        
        # Test encryption
        test_private_key = "test_private_key_12345"
        encrypted = wallet_service._encrypt_private_key(test_private_key)
        print(f"✓ Encrypted test private key")
        assert encrypted != test_private_key, "Encrypted key should differ from original"
        print(f"  - Original length: {len(test_private_key)}")
        print(f"  - Encrypted length: {len(encrypted)}")
        
        # Test decryption
        decrypted = wallet_service._decrypt_private_key(encrypted)
        print(f"✓ Decrypted private key")
        assert decrypted == test_private_key, "Decrypted key should match original"
        print(f"✓ Encryption/decryption cycle successful")
        
        # Test 6: Get decrypted private key for user
        print("\n" + "-" * 60)
        print("Test 6: Get Decrypted Private Key")
        print("-" * 60)
        
        user_private_key = wallet_service.get_decrypted_private_key(test_user.id)
        print(f"✓ Retrieved and decrypted private key for user {test_user.id}")
        assert user_private_key is not None, "Private key should not be None"
        assert len(user_private_key) > 0, "Private key should not be empty"
        print(f"  - Private key length: {len(user_private_key)}")
        
        # Test 7: Ensure user has wallet
        print("\n" + "-" * 60)
        print("Test 7: Ensure User Has Wallet")
        print("-" * 60)
        
        # Create another test user
        test_user2 = User(
            email='test2@example.com',
            google_id='google_456',
            name='Test User 2'
        )
        db_session.add(test_user2)
        db_session.commit()
        print(f"✓ Created second test user: {test_user2.id}")
        
        # Ensure wallet (should create new one)
        wallet2 = wallet_service.ensure_user_has_wallet(test_user2.id)
        print(f"✓ Ensured wallet for user {test_user2.id}")
        assert wallet2 is not None, "Wallet should be created"
        print(f"  - New wallet address: {wallet2['address']}")
        
        # Ensure wallet again (should return existing)
        wallet2_again = wallet_service.ensure_user_has_wallet(test_user2.id)
        assert wallet2_again['id'] == wallet2['id'], "Should return same wallet"
        print(f"✓ Correctly returned existing wallet on second call")
        
        # Test 8: Error handling - Invalid user
        print("\n" + "-" * 60)
        print("Test 8: Error Handling - Invalid User")
        print("-" * 60)
        
        try:
            wallet_service.create_wallet('invalid_user_id')
            print("✗ Should have raised ValueError for invalid user")
            sys.exit(1)
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {str(e)}")
        
        # Test 9: Error handling - No wallet for user
        print("\n" + "-" * 60)
        print("Test 9: Error Handling - No Wallet")
        print("-" * 60)
        
        no_wallet = wallet_service.get_user_wallet('nonexistent_user')
        assert no_wallet is None, "Should return None for user without wallet"
        print(f"✓ Correctly returned None for user without wallet")
        
        print("\n" + "=" * 60)
        print("✓ All WalletService tests passed!")
        print("=" * 60)
        
        print("\n" + "=" * 60)
        print("Implementation Summary")
        print("=" * 60)
        print("\nWalletService successfully implements:")
        print("  ✓ XRPL wallet generation (Requirement 1.3)")
        print("  ✓ Private key encryption using Fernet (Requirement 6.2)")
        print("  ✓ Secure private key storage (Requirement 6.2)")
        print("  ✓ Wallet retrieval by user ID")
        print("  ✓ Wallet retrieval by address")
        print("  ✓ Private key decryption for internal operations")
        print("  ✓ Duplicate wallet prevention")
        print("  ✓ Error handling for invalid inputs")
        print("  ✓ Integration with XRPLClient and WalletRepository")
        
        print("\nKey Features:")
        print("  • Uses cryptography.Fernet for symmetric encryption")
        print("  • Excludes private keys from public API responses")
        print("  • Provides secure decryption for transaction signing")
        print("  • Integrates with XRPL blockchain for wallet generation")
        print("  • Follows repository pattern for data access")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during verification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db_session.close()


if __name__ == '__main__':
    success = test_wallet_service()
    sys.exit(0 if success else 1)
