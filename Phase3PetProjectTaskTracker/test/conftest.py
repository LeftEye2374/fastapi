import sys
from pathlib import Path

import jwt
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Импорт src.main тянет за собой routers -> crud -> src.models.Models,
# поэтому все таблицы успевают зарегистрироваться в Base.metadata
# до того, как ниже вызывается create_all (та же история, что была
# с target_metadata в alembic/env.py).
from src.main import app
from src.core.db_core import Base, get_session


class TestSettings(BaseSettings):
    jwt_secret_key_test: str
    database_url_test: str

    class Config:
        env_file = PROJECT_ROOT / ".env"
        extra = "ignore"


test_settings = TestSettings()

test_engine = create_async_engine(
    test_settings.database_url_test,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def auth_headers(client):
    """Регистрирует и логинит тестового пользователя.
    JWT кладётся как cookie прямо в client, так что дальнейшие запросы
    этим же client уже авторизованы. Возвращает заголовок с CSRF-токеном
    для POST/PUT/DELETE (см. разбор AuthX CSRF в прошлый раз)."""
    await client.post(
        "/auth/register",
        json={"email": "test_user@test.com", "name": "Test User", "password": "pass1234"},
    )
    response = await client.post(
        "/auth/login",
        json={"email": "test_user@test.com", "password": "pass1234"},
    )
    token = response.json()["access_token"]

    payload = jwt.decode(token, options={"verify_signature": False})
    csrf = payload["csrf"]

    client.cookies.set("my_access_token", token)
    return {"X-CSRF-Token": csrf}
