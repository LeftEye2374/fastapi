from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()

async def get_session():
    async with new_session() as session:
        yield session


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

@app.post("/books")
async def add_boo():
    ...

@app.get("/books")
async def get_books():
    ...