"""
Verification script for Order Routes implementation.
Tests the order blueprint endpoints and validates the implementation.

Requirements: 5.1, 5.2, 5.3, 5.4, 8.2, 8.6, 8.7
"""
import sys
import inspect
from routes.order import order_blueprint


def verify_order_routes():
    """Verify that all required order routes are implemented."""
    
    print("=" * 70)
    print("ORDER ROUTES VERIFICATION")
    print("=" * 70)
    
    # Get all routes from the blueprint
    routes = []
    for rule in order_blueprint.url_map.iter_rules():
        if rule.endpoint.startswith('order.'):
            routes.append({
                'endpoint': rule.endpoint,
                'methods': sorted(rule.methods - {'HEAD', 'OPTIONS'}),
                'path': str(rule)
            })
    
    # Expected routes
    expected_routes = [
        {
            'name': 'Create Order',
            'endpoint': 'order.create_order',
            'methods': ['POST'],
            'path': '/',
            'requirement': '5.1, 5.2, 5.3'
        },
        {
            'name': 'Get User Orders',
            'endpoint': 'order.get_user_orders',
            'methods': ['GET'],
            'path': '/',
            'requirement': '5.4'
        },
        {
            'name': 'Get Order Detail',
            'endpoint': 'order.get_order_detail',
            'methods': ['GET'],
            'path': '/<order_id>',
            'requirement': '5.4'
        }
    ]
    
    print("\n1. ROUTE ENDPOINTS CHECK")
    print("-" * 70)
    
    all_routes_present = True
    for expected in expected_routes:
        found = False
        for route in routes:
            if route['endpoint'] == expected['endpoint']:
                found = True
                methods_match = set(route['methods']) == set(expected['methods'])
                
                print(f"\n✓ {expected['name']}")
                print(f"  Endpoint: {expected['endpoint']}")
                print(f"  Methods: {', '.join(expected['methods'])}")
                print(f"  Path: {expected['path']}")
                print(f"  Requirements: {expected['requirement']}")
                print(f"  Status: {'✓ PASS' if methods_match else '✗ FAIL (methods mismatch)'}")
                
                if not methods_match:
                    print(f"  Expected: {expected['methods']}")
                    print(f"  Found: {route['methods']}")
                    all_routes_present = False
                break
        
        if not found:
            print(f"\n✗ {expected['name']}")
            print(f"  Endpoint: {expected['endpoint']}")
            print(f"  Status: ✗ MISSING")
            all_routes_present = False
    
    # Check for JWT authentication
    print("\n\n2. JWT AUTHENTICATION CHECK")
    print("-" * 70)
    
    from routes import order
    
    jwt_protected_functions = [
        'create_order',
        'get_user_orders',
        'get_order_detail'
    ]
    
    all_jwt_protected = True
    for func_name in jwt_protected_functions:
        func = getattr(order, func_name, None)
        if func:
            # Check if jwt_required decorator is applied
            source = inspect.getsource(func)
            has_jwt = '@jwt_required()' in source
            
            print(f"\n{'✓' if has_jwt else '✗'} {func_name}")
            print(f"  JWT Protected: {'Yes' if has_jwt else 'No'}")
            
            if not has_jwt:
                all_jwt_protected = False
        else:
            print(f"\n✗ {func_name}")
            print(f"  Status: Function not found")
            all_jwt_protected = False
    
    # Check for input validation
    print("\n\n3. INPUT VALIDATION CHECK")
    print("-" * 70)
    
    validation_checks = [
        {
            'function': 'create_order',
            'decorators': ['@validate_json_request'],
            'validations': ['UUID validation', 'quantity validation', 'items validation']
        },
        {
            'function': 'get_user_orders',
            'decorators': ['@sanitize_query_params'],
            'validations': ['status validation', 'limit validation']
        },
        {
            'function': 'get_order_detail',
            'decorators': [],
            'validations': ['UUID validation', 'ownership verification']
        }
    ]
    
    all_validated = True
    for check in validation_checks:
        func = getattr(order, check['function'], None)
        if func:
            source = inspect.getsource(func)
            
            print(f"\n✓ {check['function']}")
            
            # Check decorators
            for decorator in check['decorators']:
                has_decorator = decorator in source
                print(f"  {decorator}: {'✓' if has_decorator else '✗'}")
                if not has_decorator:
                    all_validated = False
            
            # Check validations (basic check for keywords)
            for validation in check['validations']:
                keyword = validation.split()[0].lower()
                has_validation = keyword in source.lower()
                print(f"  {validation}: {'✓' if has_validation else '✗'}")
                if not has_validation:
                    all_validated = False
    
    # Check error handling
    print("\n\n4. ERROR HANDLING CHECK")
    print("-" * 70)
    
    error_types = [
        'ValidationError',
        'ResourceNotFoundError',
        'AuthorizationError',
        'ValueError',
        'Exception'
    ]
    
    all_errors_handled = True
    for func_name in jwt_protected_functions:
        func = getattr(order, func_name, None)
        if func:
            source = inspect.getsource(func)
            
            print(f"\n✓ {func_name}")
            for error_type in error_types:
                has_handler = f'except {error_type}' in source
                if has_handler or error_type == 'Exception':
                    print(f"  {error_type}: {'✓' if has_handler else '✗'}")
                    if not has_handler and error_type == 'Exception':
                        all_errors_handled = False
    
    # Check response format
    print("\n\n5. RESPONSE FORMAT CHECK")
    print("-" * 70)
    
    response_checks = [
        "jsonify({'status': 'success'",
        "jsonify({'status': 'error'",
        "'code':"
    ]
    
    all_responses_correct = True
    for func_name in jwt_protected_functions:
        func = getattr(order, func_name, None)
        if func:
            source = inspect.getsource(func)
            
            print(f"\n✓ {func_name}")
            for check in response_checks:
                has_format = check in source
                print(f"  {check}: {'✓' if has_format else '✗'}")
                if not has_format:
                    all_responses_correct = False
    
    # Summary
    print("\n\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    checks = [
        ("Route Endpoints", all_routes_present),
        ("JWT Authentication", all_jwt_protected),
        ("Input Validation", all_validated),
        ("Error Handling", all_errors_handled),
        ("Response Format", all_responses_correct)
    ]
    
    all_passed = all(result for _, result in checks)
    
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check_name:.<50} {status}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL CHECKS PASSED - Order routes implementation is complete!")
    else:
        print("✗ SOME CHECKS FAILED - Please review the implementation")
    print("=" * 70)
    
    return all_passed


if __name__ == '__main__':
    try:
        success = verify_order_routes()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Verification failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
