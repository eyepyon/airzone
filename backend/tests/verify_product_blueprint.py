"""
Verification script for Product Blueprint implementation.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def verify_product_blueprint():
    print("Product Blueprint Verification")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check 1: Import product blueprint
    print("\nChecking product blueprint import...")
    try:
        from routes.product import product_blueprint
        print("  Product blueprint imported successfully")
    except ImportError as e:
        print(f"  Failed to import product blueprint: {e}")
        all_checks_passed = False
        return all_checks_passed
    
    # Check 2: Verify blueprint name
    print("\nChecking blueprint name...")
    if product_blueprint.name == 'product':
        print("  Blueprint name is correct: 'product'")
    else:
        print(f"  Blueprint name is incorrect: '{product_blueprint.name}'")
        all_checks_passed = False
    
    # Check 3: Verify required endpoints exist
    print("\nChecking required endpoints...")
    
    required_endpoints = {
        'get_products': ('GET', '', 'Product listing'),
        'get_product_details': ('GET', '/<product_id>', 'Product details'),
        'create_product': ('POST', '', 'Product creation'),
        'update_product': ('PUT', '/<product_id>', 'Product update'),
        'delete_product': ('DELETE', '/<product_id>', 'Product deletion'),
    }
    
    blueprint_rules = {}
    for rule in product_blueprint.deferred_functions:
        func, options = rule
        endpoint_name = func.__name__
        blueprint_rules[endpoint_name] = func
    
    for endpoint_name, (method, path, description) in required_endpoints.items():
        if endpoint_name in blueprint_rules:
            print(f"  {method} {path} - {description} ({endpoint_name})")
        else:
            print(f"  Missing endpoint: {method} {path} - {description} ({endpoint_name})")
            all_checks_passed = False
    
    # Check 4: Verify blueprint registration in app.py
    print("\nChecking blueprint registration in app.py...")
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
            
        if 'from routes.product import product_blueprint' in app_content:
            print("  Product blueprint imported in app.py")
        else:
            print("  Product blueprint not imported in app.py")
            all_checks_passed = False
        
        if "app.register_blueprint(product_blueprint, url_prefix='/api/v1/products')" in app_content:
            print("  Product blueprint registered with correct URL prefix")
        else:
            print("  Product blueprint not registered or incorrect URL prefix")
            all_checks_passed = False
            
    except Exception as e:
        print(f"  Error checking app.py: {e}")
        all_checks_passed = False
    
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("All checks passed! Product blueprint is properly implemented.")
        return True
    else:
        print("Some checks failed. Please review the issues above.")
        return False


if __name__ == '__main__':
    success = verify_product_blueprint()
    sys.exit(0 if success else 1)
