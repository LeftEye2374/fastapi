import pytest


@pytest.mark.asyncio
async def test_registration_successful():
    ...

@pytest.mark.asyncio
async def test_registration_with_a_busy_email():
    ...

@pytest.mark.asyncio
async def test_login_successful():
    ...

@pytest.mark.asyncio
async def test_login_with_wrong_password():
    ...

@pytest.mark.asyncio
async def test_login_with_wrong_email():
    ...

@pytest.mark.asyncio
async def test_with_valid_token():
    ...

@pytest.mark.asyncio
async def test_without_token():
    ...