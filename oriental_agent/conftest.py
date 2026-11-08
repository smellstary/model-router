"""
Pytest 根配置。保证从仓库根目录收集 tests/ 时可以 import 各包。
"""

import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if not hasattr(types, 'FunctionType'):
    types.FunctionType = type(lambda: None)
