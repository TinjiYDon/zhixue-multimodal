import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["AUTH_REQUIRED"] = "true"
os.environ["AUTH_DEV_LOGIN"] = "true"

import asyncio

import pytest
from fastapi.testclient import TestClient

from app.core import config

config.settings = config.Settings()

from app import db as db_mod
from app.main import app
from app.services import auth_service

db_mod.configure_engine(config.settings.database_url)


@pytest.fixture
def client():
    asyncio.run(db_mod.init_db())
    auth_service.clear_sessions_for_tests()
    c = TestClient(app)
    login = c.post("/api/v1/auth/login", json={"code": "dev-test"})
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    c.headers.update({"Authorization": f"Bearer {token}"})
    return c


@pytest.fixture
def client_anon():
    """No Authorization header — for 401 tests."""
    asyncio.run(db_mod.init_db())
    auth_service.clear_sessions_for_tests()
    return TestClient(app)
