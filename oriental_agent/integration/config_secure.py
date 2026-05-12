"""
安全配置文件
不修改 OpenClaw 和 Hermes 配置的前提下安全集成
"""

SECURITY_CONFIG = {
    'server': {
        'host': '127.0.0.1',
        'port': 5000,
        'debug': True,
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
        'enabled': True,
        'allowed_ips': ['127.0.0.1', '::1', 'localhost'],
    },

    'api_keys': {
        'enabled': False,
        'required_for_external': True,
        'keys': [],
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

def load_config():
    """加载配置"""
    return {
        'security': SECURITY_CONFIG,
        'agent': ORIENTAL_AGENT_CONFIG,
    }
