from fastapi import FastAPI,    HTTPException
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

@app.get("/books")
def  read_books():
    return books

@app.get("/books/{id}")
def read_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code= 404, detail ="Книга не найдена")



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)