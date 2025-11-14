"""
Verification script for NFT Blueprint implementation.
Checks that all required endpoints are properly defined.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_nft_blueprint():
    """Verify NFT blueprint implementation"""
    print("NFT Blueprint Verification")
    print("=" * 60)
    
    try:
        # Import the blueprint
        from routes.nft import nft_blueprint
        print("✓ NFT blueprint imported successfully")
        
        # Check blueprint name
        assert nft_blueprint.name == 'nft', f"Blueprint name is '{nft_blueprint.name}', expected 'nft'"
        print("✓ Blueprint name is correct: 'nft'")
        
        # Get all routes
        routes = []
        for rule in nft_blueprint.url_map.iter_rules():
            if rule.endpoint.startswith('nft.'):
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': rule.methods - {'HEAD', 'OPTIONS'},
                    'path': rule.rule
                })
        
        print(f"\n✓ Found {len(routes)} route(s) in NFT blueprint:")
        for route in routes:
            methods_str = ', '.join(sorted(route['methods']))
            print(f"  - {methods_str} {route['path']} -> {route['endpoint']}")
        
        # Check required endpoints
        required_endpoints = [
            ('nft.get_user_nfts', 'GET', ''),
            ('nft.mint_nft', 'POST', '/mint'),
            ('nft.get_nft_details', 'GET', '/<nft_id>'),
            ('nft.get_mint_status', 'GET', '/status/<task_id>')
        ]
        
        print("\n✓ Checking required endpoints:")
        all_found = True
        for endpoint_name, method, path in required_endpoints:
            found = any(
                r['endpoint'] == endpoint_name and 
                method in r['methods']
                for r in routes
            )
            status = "✓" if found else "✗"
            print(f"  {status} {method} /api/v1/nfts{path} ({endpoint_name})")
            if not found:
                all_found = False
        
        if not all_found:
            print("\n✗ Some required endpoints are missing!")
            return False
        
        # Check if blueprint is registered in app
        print("\n✓ Checking app.py registration:")
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
            
        if 'from routes.nft import nft_blueprint' in app_content:
            print("  ✓ NFT blueprint is imported in app.py")
        else:
            print("  ✗ NFT blueprint is NOT imported in app.py")
            all_found = False
        
        if "app.register_blueprint(nft_blueprint, url_prefix='/api/v1/nfts')" in app_content:
            print("  ✓ NFT blueprint is registered with correct URL prefix")
        else:
            print("  ✗ NFT blueprint is NOT registered or has wrong URL prefix")
            all_found = False
        
        print("\n" + "=" * 60)
        if all_found:
            print("✓ All NFT blueprint requirements are met!")
            return True
        else:
            print("✗ Some NFT blueprint requirements are missing!")
            return False
            
    except Exception as e:
        print(f"\n✗ Error during verification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = verify_nft_blueprint()
    sys.exit(0 if success else 1)
