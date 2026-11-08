"""安全配置：默认 debug=False，且必须有 API Key 或 Bearer。"""

import pytest

from integration.config_secure import is_request_authorized, load_config


def _clear_auth(monkeypatch):
    for name in (
        "DEBUG",
        "API_KEYS",
        "API_KEY",
        "API_AUTH_TOKEN",
        "BEARER_TOKEN",
    ):
        monkeypatch.delenv(name, raising=False)


def test_debug_defaults_false(monkeypatch):
    _clear_auth(monkeypatch)
    monkeypatch.setenv("API_AUTH_TOKEN", "local-token")
    config = load_config(require_auth=True)
    assert config["security"]["server"]["debug"] is False
    assert config["security"]["bearer_auth"]["token"] == "local-token"
    assert config["security"]["bearer_auth"]["enabled"] is True


def test_require_api_key_or_bearer(monkeypatch):
    _clear_auth(monkeypatch)
    with pytest.raises(ValueError, match="API_KEYS"):
        load_config(require_auth=True)


def test_api_keys_alone_are_enough(monkeypatch):
    _clear_auth(monkeypatch)
    monkeypatch.setenv("API_KEYS", "alpha, beta")
    config = load_config(require_auth=True)
    security = config["security"]
    assert security["api_keys"]["keys"] == ["alpha", "beta"]
    assert security["api_keys"]["enabled"] is True
    assert security["api_keys"]["header"] == "X-API-Key"
    assert security["bearer_auth"]["enabled"] is False

    headers = {"X-API-Key": "beta"}
    assert is_request_authorized(headers, config) is True
    assert is_request_authorized({"X-API-Key": "nope"}, config) is False


def test_bearer_header(monkeypatch):
    _clear_auth(monkeypatch)
    monkeypatch.setenv("BEARER_TOKEN", "secret-token")
    config = load_config(require_auth=True)
    assert config["security"]["bearer_auth"]["token"] == "secret-token"
    assert is_request_authorized(
        {"Authorization": "Bearer secret-token"},
        config,
    ) is True
    assert is_request_authorized({"Authorization": "Bearer other"}, config) is False


def test_unconfigured_auth_rejects_everything(monkeypatch):
    _clear_auth(monkeypatch)
    config = load_config(require_auth=False)
    assert is_request_authorized({"X-API-Key": "anything"}, config) is False
    assert is_request_authorized({"Authorization": "Bearer anything"}, config) is False
