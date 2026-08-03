import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app = app),
                           base_url="htpp://test",
                           ) as cl:
        response = await cl.get("/books")
        print(response)