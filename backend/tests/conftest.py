import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

import asyncio

import pytest
from fastapi.testclient import TestClient

from app.core import config

config.settings = config.Settings()

from app import db as db_mod
from app.main import app

db_mod.configure_engine(config.settings.database_url)


@pytest.fixture
def client():
    asyncio.run(db_mod.init_db())
    return TestClient(app)
