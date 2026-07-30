from fastapi import FastAPI, Depends
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_session, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
        pass

class BookModel(Base):
    __tablename__ = "books"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str]
    author : Mapped[str]

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {"ok": True}

class BookAddSchema(BaseModel):
    title : str = Field()
    author : str = Field()

class BookSchema(BookAddSchema):
    id : int


@app.post("/books")
async def add_book(data : BookAddSchema, session : SessionDep):
    new_book = BookModel(
        title = data.title,
        author = data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}

@app.get("/books")
async def get_books():
    ...