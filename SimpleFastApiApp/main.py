from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

import uvicorn
app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Асинхронность в Python",
        "author": "Мэттью",
    },
    {
        "id": 2,
        "title": "",
        "author": "",
    },
]

@app.get("/books",
         tags=["Книги"],
         summary="Получить все книги")
def  read_books():
    return books

@app.get("/books/{id}",
         tags=["Книги"],
         summary="Получить конкретную книгу")
def read_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code= 404, detail ="Книга не найдена")


class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books",
          tags=["Книги"],
          summary="Добавить книгу")
def create_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author
    })

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)