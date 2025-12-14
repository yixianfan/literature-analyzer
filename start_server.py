#!/usr/bin/env python3
"""
启动文献整理工具服务器
"""

import uvicorn
import sys


def main():
    """启动服务器"""
    print("="*60)
    print("文献整理在线工具")
    print("="*60)
    print("\n正在启动服务器...")
    print("访问地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止服务器")
    print("="*60 + "\n")

    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
