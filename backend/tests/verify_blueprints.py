"""
Verification script to check blueprint registration without running Flask.
This script performs static analysis of the app.py file.
"""
import re
import os

def verify_blueprints():
    """Verify that all implemented blueprints are registered in app.py"""
    
    # Read app.py
    app_py_path = os.path.join(os.path.dirname(__file__), 'app.py')
    with open(app_py_path, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Expected blueprints based on completed tasks
    expected_blueprints = {
        'order': {
            'import': 'from routes.order import order_blueprint',
            'register': "app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')",
            'file': 'backend/routes/order.py'
        },
        'payment': {
            'import': 'from routes.payment import payment_blueprint',
            'register': "app.register_blueprint(payment_blueprint, url_prefix='/api/v1/payments')",
            'file': 'backend/routes/payment.py'
        },
        'wifi': {
            'import': 'from routes.wifi import wifi_blueprint',
            'register': "app.register_blueprint(wifi_blueprint, url_prefix='/api/v1/wifi')",
            'file': 'backend/routes/wifi.py'
        }
    }
    
    # Not yet implemented (tasks 8.2, 8.3, 8.4)
    not_implemented = ['auth', 'nft', 'product']
    
    print("Blueprint Registration Verification")
    print("=" * 60)
    
    all_good = True
    
    # Check implemented blueprints
    print("\n✓ Checking implemented blueprints:")
    for name, config in expected_blueprints.items():
        # Check import
        if config['import'] in app_content:
            print(f"  ✓ {name}: Import found")
        else:
            print(f"  ✗ {name}: Import NOT found")
            all_good = False
        
        # Check registration
        if config['register'] in app_content:
            print(f"  ✓ {name}: Registration found")
        else:
            print(f"  ✗ {name}: Registration NOT found")
            all_good = False
        
        # Check file exists
        if os.path.exists(config['file']):
            print(f"  ✓ {name}: Blueprint file exists")
        else:
            print(f"  ✗ {name}: Blueprint file NOT found")
            all_good = False
    
    # Check not implemented blueprints
    print(f"\n✓ Blueprints not yet implemented (expected):")
    for name in not_implemented:
        print(f"  - {name} (tasks 8.2, 8.3, 8.4 not completed)")
    
    # Check API version endpoint
    print("\n✓ Checking API version endpoint:")
    if "'/api/v1'" in app_content and "def api_version():" in app_content:
        print("  ✓ API version endpoint found")
    else:
        print("  ✗ API version endpoint NOT found")
        all_good = False
    
    # Check health check endpoint
    print("\n✓ Checking health check endpoint:")
    if "'/health'" in app_content and "def health_check():" in app_content:
        print("  ✓ Health check endpoint found")
    else:
        print("  ✗ Health check endpoint NOT found")
        all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✓ All implemented blueprints are properly registered!")
        return 0
    else:
        print("✗ Some blueprints are missing or not properly registered")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(verify_blueprints())
