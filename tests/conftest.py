from . import patch_env  # noqa
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from http_redirect_service.app import get_app
from http_redirect_service.dependencies import PoolService, get_redis_client


@pytest.fixture()
def app() -> FastAPI:
    return get_app()


@pytest.fixture()
def test_client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture()
def mock_redis_client(app, mocker) -> Mock:
    mock = mocker.AsyncMock(spec=get_redis_client)
    app.dependency_overrides[get_redis_client] = lambda: mock

    return mock


@pytest.fixture()
def mock_pool_service(app, mocker) -> Mock:
    mock = mocker.AsyncMock(spec=PoolService)
    app.dependency_overrides[PoolService] = lambda: mock

    return mock
