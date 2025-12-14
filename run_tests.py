"""
Run test script
"""

import subprocess
import sys


def run_tests():
    """Run all tests"""
    print("="*60)
    print("Run literature analyzer tests")
    print("="*60)

    try:
        # 运行pytest
        result = subprocess.run(
            ["pytest", "-v", "--tb=short"],
            capture_output=True,
            text=True
        )

        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)

        if result.returncode == 0:
            print("\n✓ All tests passed!")
        else:
            print("\n✗ Some tests failed")
            sys.exit(1)

    except FileNotFoundError:
        print("Error: pytest not found, please install test dependencies first")
        print("Run: pip install pytest pytest-asyncio")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
