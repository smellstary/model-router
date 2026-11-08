#!/usr/bin/env bash
# 本地与 CI 共用：语法编译、pytest、一次健康检查。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if command -v python >/dev/null 2>&1; then
  PY=python
else
  PY=python3
fi

"$PY" -m compileall -q .
"$PY" -m pytest
"$PY" scripts/health_check.py
