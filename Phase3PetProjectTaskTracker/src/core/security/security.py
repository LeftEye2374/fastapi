from authx import AuthX
from src.core.security.security_cfg import config
from passlib.context import CryptContext

security = AuthX(config = config)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

async def hash_password(password : str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain : str, hashed : str) -> bool:
    return pwd_context.verify(plain, hashed)