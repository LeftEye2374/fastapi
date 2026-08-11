import pytest
from fastapi import HTTPException

from src.crud.user import CRUDUser
from src.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_user_hashes_password(db_session):
    user = await CRUDUser().create_user(
        UserCreate(email="unit@test.com", name="Unit", password="pass1234"),
        db_session,
    )
    assert user.id is not None
    assert user.email == "unit@test.com"


@pytest.mark.asyncio
async def test_get_user_not_found_raises_404(db_session):
    with pytest.raises(HTTPException) as exc_info:
        await CRUDUser().get_user(999999, db_session)
    assert exc_info.value.status_code == 404
