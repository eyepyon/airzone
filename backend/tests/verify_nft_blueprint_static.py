"""
Static verification script for NFT Blueprint implementation.
Checks code structure without importing modules.
"""
import os
import re

def verify_nft_blueprint_static():
    """Verify NFT blueprint implementation using static analysis"""
    print("NFT Blueprint Static Verification")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check if nft.py exists
    nft_file = 'backend/routes/nft.py'
    if not os.path.exists(nft_file):
        print(f"✗ File not found: {nft_file}")
        return False
    
    print(f"✓ File exists: {nft_file}")
    
    # Read the file
    with open(nft_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for blueprint creation
    if 'nft_blueprint = Blueprint' in content:
        print("✓ NFT blueprint is created")
    else:
        print("✗ NFT blueprint is NOT created")
        all_checks_passed = False
    
    # Check for required endpoints
    required_endpoints = [
        ('get_user_nfts', "GET /api/v1/nfts - User's NFT list"),
        ('mint_nft', 'POST /api/v1/nfts/mint - NFT minting request'),
        ('get_nft_details', 'GET /api/v1/nfts/{id} - NFT details'),
        ('get_mint_status', 'GET /api/v1/nfts/status/{task_id} - Mint status')
    ]
    
    print("\n✓ Checking required endpoint functions:")
    for func_name, description in required_endpoints:
        pattern = rf'def {func_name}\('
        if re.search(pattern, content):
            print(f"  ✓ {description} ({func_name})")
        else:
            print(f"  ✗ {description} ({func_name}) - NOT FOUND")
            all_checks_passed = False
    
    # Check for JWT authentication
    jwt_count = content.count('@jwt_required')
    print(f"\n✓ JWT authentication decorators: {jwt_count}")
    if jwt_count >= 4:
        print("  ✓ All endpoints are protected with JWT")
    else:
        print("  ✗ Some endpoints may be missing JWT protection")
        all_checks_passed = False
    
    # Check app.py registration
    app_file = 'backend/app.py'
    if not os.path.exists(app_file):
        print(f"\n✗ File not found: {app_file}")
        return False
    
    with open(app_file, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    print("\n✓ Checking app.py registration:")
    
    if 'from routes.nft import nft_blueprint' in app_content:
        print("  ✓ NFT blueprint is imported")
    else:
        print("  ✗ NFT blueprint is NOT imported")
        all_checks_passed = False
    
    if "app.register_blueprint(nft_blueprint, url_prefix='/api/v1/nfts')" in app_content:
        print("  ✓ NFT blueprint is registered with correct URL prefix")
    else:
        print("  ✗ NFT blueprint registration not found or incorrect")
        all_checks_passed = False
    
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✓ All NFT blueprint requirements are met!")
        print("\nImplemented endpoints:")
        print("  - GET    /api/v1/nfts")
        print("  - POST   /api/v1/nfts/mint")
        print("  - GET    /api/v1/nfts/<nft_id>")
        print("  - GET    /api/v1/nfts/status/<task_id>")
        return True
    else:
        print("✗ Some requirements are not met!")
        return False


if __name__ == '__main__':
    import sys
    success = verify_nft_blueprint_static()
    sys.exit(0 if success else 1)
