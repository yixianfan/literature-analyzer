"""
运行测试脚本
"""

import subprocess
import sys


def run_tests():
    """运行所有测试"""
    print("="*60)
    print("运行文献整理工具测试")
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
            print("\n✓ 所有测试通过！")
        else:
            print("\n✗ 部分测试失败")
            sys.exit(1)

    except FileNotFoundError:
        print("错误: 未找到pytest，请先安装测试依赖")
        print("运行: pip install pytest pytest-asyncio")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
