"""
Pytest configuration for fixing Python 3.14 compatibility issues.
"""

import types

if not hasattr(types, 'FunctionType'):
    types.FunctionType = type(lambda: None)
