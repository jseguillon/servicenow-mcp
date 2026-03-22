from types import SimpleNamespace

import pytest

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.cli import create_config
from servicenow_mcp.utils.config import AuthConfig, AuthType, BearerAuthConfig


def test_auth_type_enum_includes_bearer():
    assert AuthType.BEARER == "bearer"


def test_bearer_auth_config_and_headers():
    auth_config = AuthConfig(
        type=AuthType.BEARER,
        bearer=BearerAuthConfig(token="jwt-token"),
    )

    headers = AuthManager(auth_config).get_headers()

    assert headers["Authorization"] == "Bearer jwt-token"
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"


def test_bearer_auth_supports_custom_scheme():
    auth_config = AuthConfig(
        type=AuthType.BEARER,
        bearer=BearerAuthConfig(token="opaque-token", scheme="JWT"),
    )

    headers = AuthManager(auth_config).get_headers()

    assert headers["Authorization"] == "JWT opaque-token"


def test_create_config_accepts_bearer_args():
    args = SimpleNamespace(
        instance_url="https://example.service-now.com",
        debug=False,
        timeout=30,
        auth_type="bearer",
        username=None,
        password=None,
        client_id=None,
        client_secret=None,
        token_url=None,
        api_key=None,
        api_key_header="X-ServiceNow-API-Key",
        bearer_token="edge-jwt",
        bearer_scheme="Bearer",
        script_execution_api_resource_path=None,
    )

    config = create_config(args)

    assert config.auth.type == AuthType.BEARER
    assert config.auth.bearer is not None
    assert config.auth.bearer.token == "edge-jwt"
    assert config.auth.bearer.scheme == "Bearer"


def test_create_config_requires_bearer_token():
    args = SimpleNamespace(
        instance_url="https://example.service-now.com",
        debug=False,
        timeout=30,
        auth_type="bearer",
        username=None,
        password=None,
        client_id=None,
        client_secret=None,
        token_url=None,
        api_key=None,
        api_key_header="X-ServiceNow-API-Key",
        bearer_token=None,
        bearer_scheme="Bearer",
        script_execution_api_resource_path=None,
    )

    with pytest.raises(ValueError, match="Bearer token is required"):
        create_config(args)
