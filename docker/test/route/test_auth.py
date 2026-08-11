import pytest


@pytest.mark.asyncio
async def test_registration_successful(client):
    response = await client.post(
        "/auth/register",
        json={"email": "new_user@test.com", "name": "New User", "password": "pass1234"},
    )
    assert response.status_code == 200
    assert response.json() == {"User create is successful": True}


@pytest.mark.asyncio
async def test_registration_with_a_busy_email(client):
    payload = {"email": "dup@test.com", "name": "Dup", "password": "pass1234"}

    first = await client.post("/auth/register", json=payload)
    assert first.status_code == 200

    second = await client.post("/auth/register", json=payload)
    assert second.status_code in (400, 409)


@pytest.mark.asyncio
async def test_login_successful(client):
    await client.post(
        "/auth/register",
        json={"email": "login_user@test.com", "name": "Login", "password": "pass1234"},
    )
    response = await client.post(
        "/auth/login",
        json={"email": "login_user@test.com", "password": "pass1234"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_wrong_password(client):
    await client.post(
        "/auth/register",
        json={"email": "wrongpass@test.com", "name": "WP", "password": "pass1234"},
    )
    response = await client.post(
        "/auth/login",
        json={"email": "wrongpass@test.com", "password": "not-the-password"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_with_wrong_email(client):
    response = await client.post(
        "/auth/login",
        json={"email": "does_not_exist@test.com", "password": "whatever1"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_with_valid_token(client, auth_headers):
    response = await client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "test_user@test.com"
    assert "hashed_password" not in body
    assert "password" not in body


@pytest.mark.asyncio
async def test_without_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401
