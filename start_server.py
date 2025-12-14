#!/usr/bin/env python3
"""
Start literature analyzer server
"""

import uvicorn
import sys


def main():
    """Start server"""
    print("="*60)
    print("文献整理在线工具")
    print("="*60)
    print("\n正在Start server...")
    print("Access address: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
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
        print("\n\nServer stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\nStartup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
