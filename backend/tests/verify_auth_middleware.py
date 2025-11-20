"""
Verification script for JWT authentication middleware.
Tests jwt_required decorator and get_current_user helper function.
"""
import sys
import os
from datetime import datetime, timedelta
import jwt

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, g
from middleware.auth import jwt_required, jwt_optional, get_current_user, get_current_user_id


def create_test_token(user_id: str, secret: str, expired: bool = False) -> str:
    """Create a test JWT token"""
    exp_time = datetime.utcnow() - timedelta(hours=1) if expired else datetime.utcnow() + timedelta(hours=1)
    
    payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': exp_time,
        'iat': datetime.utcnow()
    }
    
    return jwt.encode(payload, secret, algorithm='HS256')


def test_jwt_required_decorator():
    """Test jwt_required decorator"""
    print("\n=== Testing jwt_required Decorator ===")
    
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    @app.route('/protected')
    @jwt_required
    def protected_route():
        user = get_current_user()
        return {'user_id': user['user_id'], 'message': 'Success'}
    
    with app.test_client() as client:
        # Test 1: Missing token
        print("\n1. Testing missing token...")
        response = client.get('/protected')
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        data = response.get_json()
        assert data['status'] == 'error', "Expected error status"
        assert 'missing' in data['error'].lower(), "Expected 'missing' in error message"
        print("   ✓ Missing token returns 401")
        
        # Test 2: Invalid token format
        print("\n2. Testing invalid token format...")
        response = client.get('/protected', headers={'Authorization': 'InvalidFormat'})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("   ✓ Invalid format returns 401")
        
        # Test 3: Valid token
        print("\n3. Testing valid token...")
        token = create_test_token('user123', 'test-secret-key')
        response = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['user_id'] == 'user123', "Expected user_id to match"
        print("   ✓ Valid token returns 200 with user data")
        
        # Test 4: Expired token
        print("\n4. Testing expired token...")
        expired_token = create_test_token('user123', 'test-secret-key', expired=True)
        response = client.get('/protected', headers={'Authorization': f'Bearer {expired_token}'})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        data = response.get_json()
        assert 'expired' in data['error'].lower(), "Expected 'expired' in error message"
        print("   ✓ Expired token returns 401")
        
        # Test 5: Wrong secret
        print("\n5. Testing token with wrong secret...")
        wrong_token = create_test_token('user123', 'wrong-secret')
        response = client.get('/protected', headers={'Authorization': f'Bearer {wrong_token}'})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("   ✓ Token with wrong secret returns 401")
    
    print("\n✓ All jwt_required tests passed!")


def test_get_current_user():
    """Test get_current_user helper function"""
    print("\n=== Testing get_current_user Helper ===")
    
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    @app.route('/user-info')
    @jwt_required
    def user_info():
        user = get_current_user()
        user_id = get_current_user_id()
        return {
            'user': user,
            'user_id': user_id
        }
    
    with app.test_client() as client:
        # Test with valid token
        print("\n1. Testing get_current_user with valid token...")
        token = create_test_token('user456', 'test-secret-key')
        response = client.get('/user-info', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        
        assert data['user']['user_id'] == 'user456', "Expected user_id in user dict"
        assert data['user']['token_type'] == 'access', "Expected token_type in user dict"
        assert 'issued_at' in data['user'], "Expected issued_at in user dict"
        assert 'expires_at' in data['user'], "Expected expires_at in user dict"
        assert data['user_id'] == 'user456', "Expected user_id from get_current_user_id"
        print("   ✓ get_current_user returns complete user info")
        print("   ✓ get_current_user_id returns user ID")
    
    print("\n✓ All get_current_user tests passed!")


def test_jwt_optional_decorator():
    """Test jwt_optional decorator"""
    print("\n=== Testing jwt_optional Decorator ===")
    
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    @app.route('/optional')
    @jwt_optional
    def optional_route():
        user = get_current_user()
        if user:
            return {'authenticated': True, 'user_id': user['user_id']}
        return {'authenticated': False}
    
    with app.test_client() as client:
        # Test 1: No token (should succeed)
        print("\n1. Testing without token...")
        response = client.get('/optional')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['authenticated'] is False, "Expected unauthenticated"
        print("   ✓ No token returns 200 (unauthenticated)")
        
        # Test 2: Valid token (should succeed with user)
        print("\n2. Testing with valid token...")
        token = create_test_token('user789', 'test-secret-key')
        response = client.get('/optional', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['authenticated'] is True, "Expected authenticated"
        assert data['user_id'] == 'user789', "Expected user_id"
        print("   ✓ Valid token returns 200 (authenticated)")
        
        # Test 3: Invalid token (should succeed as unauthenticated)
        print("\n3. Testing with invalid token...")
        response = client.get('/optional', headers={'Authorization': 'Bearer invalid-token'})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['authenticated'] is False, "Expected unauthenticated"
        print("   ✓ Invalid token returns 200 (unauthenticated)")
    
    print("\n✓ All jwt_optional tests passed!")


def test_token_payload_validation():
    """Test token payload validation"""
    print("\n=== Testing Token Payload Validation ===")
    
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    @app.route('/protected')
    @jwt_required
    def protected_route():
        return {'message': 'Success'}
    
    with app.test_client() as client:
        # Test 1: Token without user_id
        print("\n1. Testing token without user_id...")
        payload = {
            'type': 'access',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'test-secret-key', algorithm='HS256')
        response = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("   ✓ Token without user_id rejected")
        
        # Test 2: Token with wrong type
        print("\n2. Testing token with wrong type...")
        payload = {
            'user_id': 'user123',
            'type': 'refresh',  # Wrong type
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'test-secret-key', algorithm='HS256')
        response = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        data = response.get_json()
        assert 'type' in data['error'].lower(), "Expected 'type' in error message"
        print("   ✓ Token with wrong type rejected")
    
    print("\n✓ All token validation tests passed!")


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("JWT Authentication Middleware Verification")
    print("=" * 60)
    
    try:
        test_jwt_required_decorator()
        test_get_current_user()
        test_jwt_optional_decorator()
        test_token_payload_validation()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe JWT authentication middleware is working correctly:")
        print("  • jwt_required decorator protects routes")
        print("  • get_current_user() retrieves authenticated user")
        print("  • get_current_user_id() retrieves user ID")
        print("  • jwt_optional allows optional authentication")
        print("  • Token validation works correctly")
        print("  • Error handling is proper")
        
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
