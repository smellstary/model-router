"""用 Flask 测试客户端打一次 /health，并确认未认证的业务接口会被拒绝。"""

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    fd, db_path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    os.environ["MEMORY_DB_PATH"] = db_path
    os.environ.setdefault("API_AUTH_TOKEN", "ci-health-check")

    from integration.api_server_secure import app

    client = app.test_client()
    health = client.get("/health")
    if health.status_code != 200:
        print(f"health check failed: {health.status_code} {health.data!r}")
        return 1

    denied = client.post("/api/dialog", json={"message": "你好"})
    if denied.status_code != 401:
        print(f"expected 401 without credentials, got {denied.status_code}")
        return 1

    token = os.environ["API_AUTH_TOKEN"]
    for _ in range(2):
        allowed = client.post(
            "/api/dialog",
            json={"message": "你好", "user_id": "health"},
            headers={"Authorization": f"Bearer {token}"},
        )
        if allowed.status_code != 200:
            print(f"dialog failed: {allowed.status_code} {allowed.data!r}")
            return 1

    print("health check ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
