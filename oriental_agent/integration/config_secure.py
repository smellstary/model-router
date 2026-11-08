"""
安全配置文件
不修改 OpenClaw 和 Hermes 配置的前提下安全集成

字段与环境变量对齐：
- server.debug            ← DEBUG（默认 false）
- server.host / port      ← HOST / PORT
- api_keys.keys           ← API_KEYS（逗号分隔）或 API_KEY；请求头 X-API-Key
- bearer_auth.token       ← API_AUTH_TOKEN 或 BEARER_TOKEN；请求头 Authorization: Bearer

启动时至少要配置 api_keys 或 Bearer 其中一项。load_config(require_auth=True) 会拒绝两者皆空。
"""

import os
from typing import Dict, List, Mapping, Optional


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None or not str(raw).strip():
        return default
    return str(raw).strip().lower() in ('1', 'true', 'yes', 'on')


def _split_keys(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    pieces = raw.replace(';', ',').split(',')
    return [item.strip() for item in pieces if item.strip()]


def _load_env_files() -> None:
    """读取仓库根目录与 integration/.env。已存在的环境变量优先，不覆盖。"""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(root, '.env'),
        os.path.join(root, 'integration', '.env'),
    ]
    for path in candidates:
        if not os.path.isfile(path):
            continue
        with open(path, 'r', encoding='utf-8') as handle:
            for line in handle:
                text = line.strip()
                if not text or text.startswith('#') or '=' not in text:
                    continue
                key, _, value = text.partition('=')
                key = key.strip()
                if key.startswith('export '):
                    key = key[len('export '):].strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    os.environ.setdefault(key, value)


def _collect_api_keys() -> List[str]:
    keys = _split_keys(os.environ.get('API_KEYS'))
    single = (os.environ.get('API_KEY') or '').strip()
    if single and single not in keys:
        keys.append(single)
    return keys


def _collect_bearer_token() -> str:
    return (os.environ.get('API_AUTH_TOKEN') or os.environ.get('BEARER_TOKEN') or '').strip()


def load_config(require_auth: bool = False) -> Dict:
    """
    加载安全配置与智能体集成配置。

    require_auth=True 时，api_keys 与 Bearer 都未设置会抛出 ValueError。
    """
    _load_env_files()

    debug = _env_flag('DEBUG', False)
    host = os.environ.get('HOST', '127.0.0.1').strip() or '127.0.0.1'
    port = int(os.environ.get('PORT', '5000') or '5000')
    api_keys = _collect_api_keys()
    bearer = _collect_bearer_token()

    if require_auth and not api_keys and not bearer:
        raise ValueError(
            '安全配置不完整：至少需要设置 API_KEYS（或 API_KEY）或 '
            'API_AUTH_TOKEN（Bearer，也接受 BEARER_TOKEN）。'
            'DEBUG 默认 false。参见 integration/.env.example。'
        )

    trusted = [
        item.strip()
        for item in os.environ.get('TRUSTED_IPS', '127.0.0.1,::1,localhost').split(',')
        if item.strip()
    ]
    ip_whitelist_enabled = _env_flag('ENABLE_IP_WHITELIST', False)
    rate_enabled = _env_flag('ENABLE_RATE_LIMITING', True)
    requests_per_minute = int(os.environ.get('RATE_LIMIT_PER_MINUTE', '60') or '60')
    requests_per_hour = int(os.environ.get('RATE_LIMIT_PER_HOUR', '1000') or '1000')
    max_request_size = int(os.environ.get('MAX_REQUEST_SIZE_BYTES', str(1024 * 1024)) or 1024 * 1024)

    security = {
        'server': {
            'host': host,
            'port': port,
            'debug': debug,
        },
        'trusted_ips': trusted,
        'enable_ip_whitelist': ip_whitelist_enabled,
        'ip_whitelist': {
            'enabled': ip_whitelist_enabled,
            'allowed_ips': trusted,
        },
        'enable_rate_limiting': rate_enabled,
        'rate_limiting': {
            'enabled': rate_enabled,
            'requests_per_minute': requests_per_minute,
            'requests_per_hour': requests_per_hour,
        },
        'rate_limit': {
            'requests_per_minute': requests_per_minute,
            'requests_per_hour': requests_per_hour,
        },
        'enable_input_validation': _env_flag('ENABLE_INPUT_VALIDATION', True),
        'input_validation': {
            'enabled': True,
            'max_text_length': 10000,
            'max_list_length': 1000,
            'max_request_size_bytes': max_request_size,
        },
        'max_request_size': max_request_size,
        'enable_request_logging': True,
        'enable_security_headers': True,
        'cors': {
            'enabled': True,
            'origins': ['http://localhost:*', 'http://127.0.0.1:*'],
        },
        'logging': {
            'enabled': True,
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'security_headers': {
            'enabled': True,
            'x_frame_options': 'DENY',
            'x_content_type_options': 'nosniff',
            'x_xss_protection': '1; mode=block',
            'strict_transport_security': 'max-age=31536000; includeSubDomains',
        },
        'api_keys': {
            'enabled': bool(api_keys),
            'required_for_external': True,
            'header': 'X-API-Key',
            'keys': api_keys,
        },
        'bearer_auth': {
            'enabled': bool(bearer),
            'header': 'Authorization',
            'scheme': 'Bearer',
            'token': bearer,
        },
    }

    return {
        'security': security,
        'agent': ORIENTAL_AGENT_CONFIG,
    }


def is_request_authorized(headers: Mapping[str, str], config: Optional[Dict] = None) -> bool:
    """
    校验 X-API-Key 或 Authorization: Bearer。
    两者都没配置时一律拒绝（健康检查由调用方自行放行）。
    """
    loaded = config or load_config(require_auth=False)
    security = loaded.get('security', loaded)
    keys = list(security.get('api_keys', {}).get('keys') or [])
    token = (security.get('bearer_auth', {}).get('token') or '').strip()
    if not keys and not token:
        return False

    supplied_key = (headers.get('X-API-Key') or headers.get('x-api-key') or '').strip()
    if supplied_key and supplied_key in keys:
        return True

    authorization = headers.get('Authorization') or headers.get('authorization') or ''
    parts = authorization.split(None, 1)
    supplied_bearer = parts[1].strip() if len(parts) == 2 and parts[0].lower() == 'bearer' else ''
    if token and supplied_bearer and supplied_bearer == token:
        return True
    return False


# 静态默认值。运行时以 load_config() 为准，这里只保留与生产姿态一致的默认 debug=False。
SECURITY_CONFIG = {
    'server': {
        'host': '127.0.0.1',
        'port': 5000,
        'debug': False,
    },

    'trusted_ips': [
        '127.0.0.1',
        '::1',
        'localhost',
    ],

    'rate_limiting': {
        'enabled': True,
        'requests_per_minute': 60,
        'requests_per_hour': 1000,
    },

    'input_validation': {
        'enabled': True,
        'max_text_length': 10000,
        'max_list_length': 1000,
        'max_request_size_bytes': 1024 * 1024,
    },

    'cors': {
        'enabled': True,
        'origins': ['http://localhost:*', 'http://127.0.0.1:*'],
    },

    'logging': {
        'enabled': True,
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    },

    'security_headers': {
        'enabled': True,
        'x_frame_options': 'DENY',
        'x_content_type_options': 'nosniff',
        'x_xss_protection': '1; mode=block',
        'strict_transport_security': 'max-age=31536000; includeSubDomains',
    },

    'ip_whitelist': {
        'enabled': False,
        'allowed_ips': ['127.0.0.1', '::1', 'localhost'],
    },

    'api_keys': {
        'enabled': False,
        'required_for_external': True,
        'header': 'X-API-Key',
        'keys': [],
    },

    'bearer_auth': {
        'enabled': False,
        'header': 'Authorization',
        'scheme': 'Bearer',
        'token': '',
    },
}

ORIENTAL_AGENT_CONFIG = {
    'integration': {
        'openclaw': {
            'webhook_endpoint': '/webhook/openclaw',
            'timeout': 30,
        },
        'hermes': {
            'commercial_endpoint': '/hermes/commercial',
            'avatar_endpoint': '/hermes/avatar',
            'timeout': 30,
        },
    },

    'features': {
        'commercial_analysis': True,
        'avatar_system': True,
        'image_rendering': True,
    },

    'commercial': {
        'max_opportunities': 10,
        'max_investment_projects': 5,
        'enable_caching': True,
        'cache_ttl': 3600,
    },

    'avatar': {
        'max_avatars': 50,
        'export_formats': ['svg', 'json'],
        'default_preset': 'model_a',
    },
}
