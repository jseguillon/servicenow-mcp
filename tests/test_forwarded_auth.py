from types import SimpleNamespace

import pytest

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.auth.request_context import forwarded_auth_header
from servicenow_mcp.cli import create_config
from servicenow_mcp.utils.config import AuthConfig, AuthType


def test_auth_type_enum_includes_bearer():
    assert AuthType.BEARER == "bearer"


def test_bearer_auth_forwards_incoming_header():
    auth_config = AuthConfig(type=AuthType.BEARER)

    with forwarded_auth_header("Bearer jwt-from-mcp"):
        headers = AuthManager(auth_config).get_headers()

    assert headers["Authorization"] == "Bearer jwt-from-mcp"
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"


def test_bearer_auth_requires_incoming_header():
    auth_config = AuthConfig(type=AuthType.BEARER)

    with pytest.raises(ValueError, match="incoming MCP Authorization header"):
        AuthManager(auth_config).get_headers()


def test_create_config_accepts_bearer_without_static_token():
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
        script_execution_api_resource_path=None,
    )

    config = create_config(args)

    assert config.auth.type == AuthType.BEARER
