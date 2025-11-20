"""
Run all tests for implemented features
"""
import os
import sys
import subprocess

def run_test(test_name: str, script_path: str) -> bool:
    """Run a test script and return result"""
    print("\n" + "="*60)
    print(f"Running: {test_name}")
    print("="*60)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(__file__),
            capture_output=False,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            print(f"\n✓ {test_name} PASSED")
        else:
            print(f"\n✗ {test_name} FAILED")
        
        return success
        
    except Exception as e:
        print(f"\n✗ {test_name} ERROR: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("Running All Tests")
    print("="*60)
    
    tests = [
        ("Wallet Generation Test", "test_wallet_generation.py"),
        ("XRPL Functions Test", "test_xrpl_functions.py"),
    ]
    
    results = []
    
    for test_name, script_path in tests:
        success = run_test(test_name, script_path)
        results.append((test_name, success))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
