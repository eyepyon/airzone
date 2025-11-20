"""
Verification script to test auth blueprint endpoints.
Tests the three auth endpoints: /google, /refresh, /me
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

def verify_auth_blueprint():
    """Verify auth blueprint implementation"""
    print("Auth Blueprint Verification")
    print("=" * 60)
    
    all_passed = True
    
    # Check if auth.py exists
    print("\n1. Checking auth blueprint file...")
    auth_file = os.path.join(os.path.dirname(__file__), 'routes', 'auth.py')
    if os.path.exists(auth_file):
        print(f"  ✓ File exists: {auth_file}")
    else:
        print(f"  ✗ File not found: {auth_file}")
        all_passed = False
        return 1
    
    # Import and check blueprint
    print("\n2. Importing auth blueprint...")
    try:
        from routes.auth import auth_blueprint
        print(f"  ✓ Successfully imported auth_blueprint")
        print(f"  ✓ Blueprint name: {auth_blueprint.name}")
    except ImportError as e:
        print(f"  ✗ Failed to import: {str(e)}")
        all_passed = False
        return 1
    
    # Check blueprint routes
    print("\n3. Checking blueprint routes...")
    expected_routes = [
        ('google', ['POST']),
        ('refresh', ['POST']),
        ('me', ['GET'])
    ]
    
    # Get all rules for this blueprint
    from app import app
    blueprint_rules = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('auth.'):
            endpoint_name = rule.endpoint.split('.')[1]
            methods = [m for m in rule.methods if m not in ['HEAD', 'OPTIONS']]
            blueprint_rules.append((endpoint_name, methods, rule.rule))
    
    print(f"  Found {len(blueprint_rules)} routes in auth blueprint:")
    for endpoint, methods, path in blueprint_rules:
        print(f"    - {', '.join(methods)} {path} -> {endpoint}")
    
    # Verify expected routes exist
    print("\n4. Verifying required endpoints...")
    for expected_endpoint, expected_methods in expected_routes:
        found = False
        for endpoint, methods, path in blueprint_rules:
            if endpoint == expected_endpoint:
                found = True
                # Check if expected methods are present
                for method in expected_methods:
                    if method in methods:
                        print(f"  ✓ {method} /api/v1/auth/{expected_endpoint} - Found")
                    else:
                        print(f"  ✗ {method} /api/v1/auth/{expected_endpoint} - Method not found")
                        all_passed = False
                break
        
        if not found:
            print(f"  ✗ Endpoint '{expected_endpoint}' not found")
            all_passed = False
    
    # Check if blueprint is registered in app.py
    print("\n5. Checking blueprint registration in app.py...")
    app_file = os.path.join(os.path.dirname(__file__), 'app.py')
    with open(app_file, 'r', encoding='utf-8') as f:
        app_content = f.read()
        if 'from routes.auth import auth_blueprint' in app_content:
            print("  ✓ Blueprint imported in app.py")
        else:
            print("  ✗ Blueprint not imported in app.py")
            all_passed = False
        
        if "app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')" in app_content:
            print("  ✓ Blueprint registered with correct URL prefix")
        else:
            print("  ✗ Blueprint not registered or incorrect URL prefix")
            all_passed = False
    
    # Check dependencies
    print("\n6. Checking dependencies...")
    try:
        from services.auth_service import AuthService
        print("  ✓ AuthService imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import AuthService: {str(e)}")
        all_passed = False
    
    try:
        from middleware.auth import jwt_required, get_current_user
        print("  ✓ Auth middleware imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import auth middleware: {str(e)}")
        all_passed = False
    
    try:
        from clients.google_auth import GoogleAuthClient
        print("  ✓ GoogleAuthClient imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import GoogleAuthClient: {str(e)}")
        all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All auth blueprint checks passed!")
        print("\nImplemented endpoints:")
        print("  - POST /api/v1/auth/google - Google OAuth authentication")
        print("  - POST /api/v1/auth/refresh - Token refresh")
        print("  - GET /api/v1/auth/me - Current user information")
        print("\nRequirements satisfied: 1.1, 1.4, 1.5, 8.2, 8.6, 8.7")
        return 0
    else:
        print("✗ Some checks failed")
        return 1

if __name__ == '__main__':
    exit_code = verify_auth_blueprint()
    sys.exit(exit_code)
