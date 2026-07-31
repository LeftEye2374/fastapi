from sqlalchemy import Column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped
from fastapi import FastAPI

app = FastAPI()

engine = create_async_engine("sqlite + aiosqlite:///books.db")


new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "books"

    id : Mapped[int] = Column(primary_key=True)
    title : Mapped[str]
    author : Mapped[str]


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_async(Base.metadata.drop_all)
        await connection.run_async(Base.metadata.create_all)
