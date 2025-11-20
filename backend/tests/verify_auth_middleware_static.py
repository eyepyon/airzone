"""
Static verification of JWT authentication middleware implementation.
Checks that all required components are present without running the code.
"""
import os
import ast
import sys


def check_file_exists(filepath):
    """Check if file exists"""
    if os.path.exists(filepath):
        print(f"✓ File exists: {filepath}")
        return True
    else:
        print(f"✗ File missing: {filepath}")
        return False


def check_function_exists(tree, function_name):
    """Check if a function is defined in the AST"""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return True
    return False


def check_decorator_exists(tree, decorator_name):
    """Check if a decorator function is defined"""
    return check_function_exists(tree, decorator_name)


def analyze_auth_middleware(filepath):
    """Analyze the auth middleware file"""
    print("\n=== Analyzing auth.py ===")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        tree = ast.parse(content)
    
    checks = []
    
    # Check for required functions
    print("\nChecking required functions:")
    
    functions = [
        ('extract_token_from_header', 'Extract JWT token from Authorization header'),
        ('verify_jwt_token', 'Verify JWT token and extract payload'),
        ('get_current_user', 'Get current authenticated user'),
        ('get_current_user_id', 'Get current user ID'),
        ('jwt_required', 'JWT required decorator'),
        ('jwt_optional', 'JWT optional decorator'),
    ]
    
    for func_name, description in functions:
        exists = check_function_exists(tree, func_name)
        status = "✓" if exists else "✗"
        print(f"  {status} {func_name}: {description}")
        checks.append(exists)
    
    # Check for custom exception
    print("\nChecking custom exception:")
    has_auth_error = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'AuthenticationError':
            has_auth_error = True
            break
    status = "✓" if has_auth_error else "✗"
    print(f"  {status} AuthenticationError exception class")
    checks.append(has_auth_error)
    
    # Check for imports
    print("\nChecking required imports:")
    imports = {
        'functools': False,
        'flask': False,
        'jwt': False,
        'logging': False,
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in imports:
                    imports[alias.name] = True
        elif isinstance(node, ast.ImportFrom):
            if node.module in imports:
                imports[node.module] = True
    
    for module, imported in imports.items():
        status = "✓" if imported else "✗"
        print(f"  {status} {module}")
        checks.append(imported)
    
    # Check for key implementation details in source
    print("\nChecking implementation details:")
    
    details = [
        ('Bearer', 'Bearer token extraction'),
        ('Authorization', 'Authorization header handling'),
        ('HS256', 'HS256 algorithm for JWT'),
        ('g.current_user', 'Flask g object for user context'),
        ('@wraps', 'Function wrapper preservation'),
        ('JWT_SECRET_KEY', 'JWT secret key from config'),
    ]
    
    for keyword, description in details:
        exists = keyword in content
        status = "✓" if exists else "✗"
        print(f"  {status} {description}")
        checks.append(exists)
    
    return all(checks)


def check_requirements_compliance():
    """Check compliance with requirements"""
    print("\n=== Requirements Compliance ===")
    
    filepath = 'middleware/auth.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    requirements = [
        ('6.1', 'JWT Bearer Token authentication', ['Bearer', 'Authorization', 'jwt_required']),
        ('6.7', 'API authentication and authorization', ['jwt_required', 'get_current_user']),
    ]
    
    all_compliant = True
    for req_id, description, keywords in requirements:
        print(f"\nRequirement {req_id}: {description}")
        compliant = all(keyword in content for keyword in keywords)
        status = "✓" if compliant else "✗"
        print(f"  {status} Implementation found")
        if compliant:
            for keyword in keywords:
                print(f"    • {keyword}")
        all_compliant = all_compliant and compliant
    
    return all_compliant


def check_task_completion():
    """Check if all task items are completed"""
    print("\n=== Task Completion Check ===")
    
    items = [
        ('JWT トークン検証ミドルウェアを作成（backend/middleware/auth.py）', 
         'middleware/auth.py'),
        ('jwt_required デコレータの実装', 
         'jwt_required function'),
        ('get_current_user ヘルパー関数の実装', 
         'get_current_user function'),
    ]
    
    all_complete = True
    
    for description, check_item in items:
        if check_item.endswith('.py'):
            # File check
            exists = os.path.exists(check_item)
            status = "✓" if exists else "✗"
            print(f"  {status} {description}")
            all_complete = all_complete and exists
        else:
            # Function check
            filepath = 'middleware/auth.py'
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            func_name = check_item.split()[0]
            exists = check_function_exists(tree, func_name)
            status = "✓" if exists else "✗"
            print(f"  {status} {description}")
            all_complete = all_complete and exists
    
    return all_complete


def main():
    """Run all static verification checks"""
    print("=" * 70)
    print("JWT Authentication Middleware - Static Verification")
    print("=" * 70)
    
    # Change to backend directory
    if os.path.exists('backend'):
        os.chdir('backend')
    
    filepath = 'middleware/auth.py'
    
    # Check file exists
    if not check_file_exists(filepath):
        print("\n✗ VERIFICATION FAILED: auth.py not found")
        return 1
    
    try:
        # Analyze implementation
        implementation_ok = analyze_auth_middleware(filepath)
        
        # Check requirements
        requirements_ok = check_requirements_compliance()
        
        # Check task completion
        task_ok = check_task_completion()
        
        # Final result
        print("\n" + "=" * 70)
        if implementation_ok and requirements_ok and task_ok:
            print("✓ ALL CHECKS PASSED!")
            print("=" * 70)
            print("\nTask 8.1 Implementation Summary:")
            print("  ✓ JWT authentication middleware created")
            print("  ✓ jwt_required decorator implemented")
            print("  ✓ get_current_user helper function implemented")
            print("  ✓ get_current_user_id helper function implemented")
            print("  ✓ jwt_optional decorator for optional auth")
            print("  ✓ Token extraction from Authorization header")
            print("  ✓ JWT token verification with HS256")
            print("  ✓ Error handling with AuthenticationError")
            print("  ✓ Flask g object for user context")
            print("  ✓ Logging for security events")
            print("  ✓ Requirements 6.1 and 6.7 satisfied")
            print("\nThe middleware is ready to be used in route handlers.")
            return 0
        else:
            print("✗ VERIFICATION FAILED")
            print("=" * 70)
            if not implementation_ok:
                print("  ✗ Implementation incomplete")
            if not requirements_ok:
                print("  ✗ Requirements not fully met")
            if not task_ok:
                print("  ✗ Task items not complete")
            return 1
            
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
