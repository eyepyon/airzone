"""
Verification script for payment routes implementation.
Tests the payment blueprint endpoints.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_payment_routes():
    """Verify payment routes implementation"""
    print("=" * 60)
    print("Payment Routes Verification")
    print("=" * 60)
    
    try:
        # Import payment blueprint
        from routes.payment import payment_blueprint
        print("✓ Payment blueprint imported successfully")
        
        # Check blueprint name
        assert payment_blueprint.name == 'payment', "Blueprint name should be 'payment'"
        print("✓ Blueprint name is correct")
        
        # Check routes
        routes = [rule.rule for rule in payment_blueprint.url_map.iter_rules()]
        print(f"\n✓ Blueprint has {len(routes)} routes")
        
        # Verify required endpoints exist
        required_endpoints = [
            'payment.create_payment_intent',
            'payment.handle_stripe_webhook',
            'payment.get_payment'
        ]
        
        endpoint_names = [rule.endpoint for rule in payment_blueprint.url_map.iter_rules()]
        
        for endpoint in required_endpoints:
            if endpoint in endpoint_names:
                print(f"✓ Endpoint '{endpoint}' exists")
            else:
                print(f"✗ Endpoint '{endpoint}' missing")
        
        print("\n" + "=" * 60)
        print("Payment Routes Verification Complete")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = verify_payment_routes()
    sys.exit(0 if success else 1)



def test_route_structure():
    """Test the structure of payment routes"""
    print("\n" + "=" * 60)
    print("Testing Route Structure")
    print("=" * 60)
    
    try:
        from routes.payment import payment_blueprint
        
        # Get all rules
        rules = list(payment_blueprint.url_map.iter_rules())
        
        print(f"\nFound {len(rules)} routes:")
        for rule in rules:
            print(f"  - {rule.rule} [{', '.join(rule.methods - {'HEAD', 'OPTIONS'})}]")
            print(f"    Endpoint: {rule.endpoint}")
        
        # Check specific routes
        route_checks = {
            '/intent': ['POST'],
            '/webhook': ['POST'],
            '/<payment_id>': ['GET']
        }
        
        print("\nRoute validation:")
        for route_path, expected_methods in route_checks.items():
            matching_rules = [r for r in rules if route_path in r.rule]
            if matching_rules:
                rule = matching_rules[0]
                actual_methods = rule.methods - {'HEAD', 'OPTIONS'}
                if set(expected_methods).issubset(actual_methods):
                    print(f"✓ {route_path} supports {expected_methods}")
                else:
                    print(f"✗ {route_path} missing methods: {set(expected_methods) - actual_methods}")
            else:
                print(f"✗ Route {route_path} not found")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Route structure test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = verify_payment_routes()
    if success:
        success = test_route_structure()
    sys.exit(0 if success else 1)
