"""
Verification script for AuthService implementation.
Tests Google OAuth authentication flow, JWT token generation and verification.

Requirements: 1.1, 1.4, 1.5, 6.1
"""
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import only what we need, with mocking for dependencies
import jwt


def test_auth_service():
    """Test AuthService functionality"""
    print("=" * 60)
    print("AuthService Verification")
    print("=" * 60)
    
    # Mock dependencies
    db_session = Mock()
    google_client = Mock()
    jwt_secret = "test-secret-key"
    
    # Mock the repositories and models
    sys.modules['models'] = Mock()
    sys.modules['models.base'] = Mock()
    sys.modules['models.user'] = Mock()
    sys.modules['models.wallet'] = Mock()
    sys.modules['repositories'] = Mock()
    sys.modules['repositories.base'] = Mock()
    sys.modules['repositories.user_repository'] = Mock()
    sys.modules['repositories.wallet_repository'] = Mock()
    sys.modules['clients'] = Mock()
    sys.modules['clients.google_auth'] = Mock()
    
    # Now import AuthService
    from services.auth_service import AuthService
    
    # Create AuthService instance
    auth_service = AuthService(
        db_session=db_session,
        google_client=google_client,
        jwt_secret=jwt_secret,
        jwt_access_expires=3600,  # 1 hour
        jwt_refresh_expires=2592000  # 30 days
    )
    
    print("\n✓ AuthService instance created successfully")
    
    # Test 1: JWT Access Token Generation
    print("\n" + "-" * 60)
    print("Test 1: JWT Access Token Generation (Requirement 1.4)")
    print("-" * 60)
    
    user_id = "test-user-123"
    access_token = auth_service.create_access_token(user_id)
    
    print(f"✓ Access token generated: {access_token[:50]}...")
    print(f"✓ Token type: {type(access_token)}")
    
    # Verify token structure
    payload = auth_service.verify_access_token(access_token)
    print(f"✓ Token verified successfully")
    print(f"  - User ID: {payload['user_id']}")
    print(f"  - Token Type: {payload['type']}")
    print(f"  - Issued At: {datetime.fromtimestamp(payload['iat'])}")
    print(f"  - Expires At: {datetime.fromtimestamp(payload['exp'])}")
    
    # Verify expiration is 1 hour
    exp_time = datetime.fromtimestamp(payload['exp'])
    iat_time = datetime.fromtimestamp(payload['iat'])
    duration = (exp_time - iat_time).total_seconds()
    assert duration == 3600, f"Expected 3600 seconds, got {duration}"
    print(f"✓ Access token expiration: {duration} seconds (1 hour) ✓")
    
    # Test 2: JWT Refresh Token Generation
    print("\n" + "-" * 60)
    print("Test 2: JWT Refresh Token Generation (Requirement 1.5)")
    print("-" * 60)
    
    refresh_token = auth_service.create_refresh_token(user_id)
    
    print(f"✓ Refresh token generated: {refresh_token[:50]}...")
    
    # Verify token structure
    payload = auth_service.verify_refresh_token(refresh_token)
    print(f"✓ Token verified successfully")
    print(f"  - User ID: {payload['user_id']}")
    print(f"  - Token Type: {payload['type']}")
    
    # Verify expiration is 30 days
    exp_time = datetime.fromtimestamp(payload['exp'])
    iat_time = datetime.fromtimestamp(payload['iat'])
    duration = (exp_time - iat_time).total_seconds()
    assert duration == 2592000, f"Expected 2592000 seconds, got {duration}"
    print(f"✓ Refresh token expiration: {duration} seconds (30 days) ✓")
    
    # Test 3: Token Verification
    print("\n" + "-" * 60)
    print("Test 3: Token Verification (Requirement 6.1)")
    print("-" * 60)
    
    # Test valid access token
    try:
        payload = auth_service.verify_access_token(access_token)
        print(f"✓ Valid access token verified successfully")
    except ValueError as e:
        print(f"✗ Failed to verify valid token: {e}")
        sys.exit(1)
    
    # Test invalid token
    try:
        auth_service.verify_access_token("invalid-token")
        print(f"✗ Invalid token should have raised ValueError")
        sys.exit(1)
    except ValueError:
        print(f"✓ Invalid token correctly rejected")
    
    # Test wrong token type (using refresh token as access token)
    try:
        auth_service.verify_access_token(refresh_token)
        print(f"✗ Wrong token type should have raised ValueError")
        sys.exit(1)
    except ValueError:
        print(f"✓ Wrong token type correctly rejected")
    
    # Test 4: Token Refresh
    print("\n" + "-" * 60)
    print("Test 4: Token Refresh (Requirement 1.5)")
    print("-" * 60)
    
    # Mock user repository
    mock_user = Mock()
    mock_user.id = user_id
    auth_service.user_repo.find_by_id = Mock(return_value=mock_user)
    
    new_access_token = auth_service.refresh_access_token(refresh_token)
    print(f"✓ New access token generated from refresh token")
    print(f"  - New token: {new_access_token[:50]}...")
    
    # Verify new token is valid
    new_payload = auth_service.verify_access_token(new_access_token)
    assert new_payload['user_id'] == user_id
    print(f"✓ New access token is valid and contains correct user_id")
    
    # Test 5: Google OAuth Authentication Flow
    print("\n" + "-" * 60)
    print("Test 5: Google OAuth Authentication (Requirement 1.1)")
    print("-" * 60)
    
    # Mock Google client response
    google_user_info = {
        'google_id': 'google-123',
        'email': 'test@example.com',
        'email_verified': True,
        'name': 'Test User'
    }
    google_client.verify_id_token = Mock(return_value=google_user_info)
    
    # Mock user repository for new user
    mock_new_user = Mock()
    mock_new_user.id = "new-user-456"
    mock_new_user.email = google_user_info['email']
    mock_new_user.name = google_user_info['name']
    mock_new_user.to_dict = Mock(return_value={
        'id': mock_new_user.id,
        'email': mock_new_user.email,
        'name': mock_new_user.name
    })
    
    auth_service.user_repo.find_by_google_id = Mock(return_value=None)
    auth_service.user_repo.create_user = Mock(return_value=mock_new_user)
    db_session.commit = Mock()
    
    # Test authentication
    id_token = "mock-google-id-token"
    user_dict, access_token, refresh_token = auth_service.authenticate_google(id_token)
    
    print(f"✓ Google OAuth authentication successful")
    print(f"  - User: {user_dict}")
    print(f"  - Access Token: {access_token[:50]}...")
    print(f"  - Refresh Token: {refresh_token[:50]}...")
    
    # Verify tokens are valid
    access_payload = auth_service.verify_access_token(access_token)
    refresh_payload = auth_service.verify_refresh_token(refresh_token)
    
    assert access_payload['user_id'] == mock_new_user.id
    assert refresh_payload['user_id'] == mock_new_user.id
    print(f"✓ Generated tokens are valid and contain correct user_id")
    
    # Test 6: Get Current User
    print("\n" + "-" * 60)
    print("Test 6: Get Current User (Requirement 6.1)")
    print("-" * 60)
    
    auth_service.user_repo.find_by_id = Mock(return_value=mock_new_user)
    
    current_user = auth_service.get_current_user(access_token)
    print(f"✓ Current user retrieved successfully")
    print(f"  - User: {current_user}")
    
    assert current_user['id'] == mock_new_user.id
    print(f"✓ Current user data is correct")
    
    # Test 7: Token Validation
    print("\n" + "-" * 60)
    print("Test 7: Token Validation")
    print("-" * 60)
    
    is_valid = auth_service.validate_token(access_token)
    assert is_valid == True
    print(f"✓ Valid token validation: {is_valid}")
    
    is_invalid = auth_service.validate_token("invalid-token")
    assert is_invalid == False
    print(f"✓ Invalid token validation: {is_invalid}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print("✓ All tests passed successfully!")
    print("\nRequirements Verified:")
    print("  ✓ 1.1 - Google OAuth authentication flow")
    print("  ✓ 1.4 - JWT access token generation (1 hour expiration)")
    print("  ✓ 1.5 - JWT refresh token generation (30 days expiration)")
    print("  ✓ 6.1 - JWT token verification and user authentication")
    print("\nAuthService Implementation: COMPLETE ✓")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_auth_service()
    except Exception as e:
        print(f"\n✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
