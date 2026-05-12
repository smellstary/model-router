#!/usr/bin/env python3
"""
安全启动脚本
启动东方智慧智能体 API 服务（安全增强版）
不修改 OpenClaw 和 Hermes 配置
"""

import os
import sys
import signal
import subprocess
import time
import requests
from datetime import datetime


def check_port(port):
    """检查端口是否被占用"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', port))
        sock.close()
        return True
    except OSError:
        return False


def wait_for_service(url, timeout=30):
    """等待服务启动"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False


def main():
    """主函数"""
    print("=" * 60)
    print("🛡️  东方智慧智能体 - 安全启动")
    print("=" * 60)

    port = 5000

    if not check_port(port):
        print(f"❌ 端口 {port} 已被占用")
        print("请先停止占用端口的进程，或修改端口配置")
        return False

    server_script = os.path.join(os.path.dirname(__file__), 'api_server_secure.py')

    if not os.path.exists(server_script):
        print(f"❌ 找不到服务器脚本: {server_script}")
        return False

    print("🚀 正在启动安全 API 服务...")
    print()

    process = subprocess.Popen(
        [sys.executable, server_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )

    service_url = f"http://localhost:{port}/health"
    print(f"⏳ 等待服务启动...")

    if wait_for_service(service_url, timeout=30):
        print()
        print("=" * 60)
        print("✅ 服务启动成功！")
        print("=" * 60)
        print()
        print("📍 服务地址:")
        print(f"   - API 基础地址: http://localhost:{port}")
        print(f"   - OpenClaw Webhook: http://localhost:{port}/webhook/openclaw")
        print(f"   - Hermes 接口: http://localhost:{port}/hermes/commercial")
        print(f"   - 健康检查: http://localhost:{port}/health")
        print()
        print("🔒 安全特性:")
        print("   - IP 白名单保护")
        print("   - 请求频率限制")
        print("   - 输入验证和清洗")
        print("   - 安全响应头")
        print("   - 详细请求日志")
        print()
        print("=" * 60)
        print("📝 按 Ctrl+C 停止服务")
        print("=" * 60)
        print()

        def signal_handler(sig, frame):
            print()
            print("🛑 正在停止服务...")
            process.terminate()
            process.wait()
            print("✅ 服务已停止")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        try:
            for line in process.stdout:
                print(line, end='')
        except KeyboardInterrupt:
            signal_handler(None, None)

    else:
        print()
        print("❌ 服务启动失败")
        print("请检查日志以获取更多信息")
        process.terminate()
        process.wait()
        return False

    return True


if __name__ == '__main__':
    main()
