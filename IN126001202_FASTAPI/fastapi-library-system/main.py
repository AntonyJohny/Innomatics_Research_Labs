from fastapi import FastAPI, HTTPException, Query, Path, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Library Management System - Innomatics Internship")

class Book(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    author: str
    category: str
    is_borrowed: bool = False
    borrower_name: Optional[str] = None

class BookCreate(BaseModel):
    title: str
    author: str
    category: str

db_books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Fiction", "is_borrowed": False, "borrower_name": None},
    {"id": 2, "title": "FastAPI Essentials", "author": "John Doe", "category": "Tech", "is_borrowed": False, "borrower_name": None},
    {"id": 3, "title": "Python 101", "author": "Guido Van", "category": "Tech", "is_borrowed": True, "borrower_name": "Alice"},
]

def find_book(book_id: int):
    return next((b for b in db_books if b["id"] == book_id), None)


@app.get("/", tags=["General"])
def home():
    return {"message": "Welcome to the Library Book System API"}

@app.get("/books", response_model=List[Book], tags=["Inventory"])
def get_all_books():
    return db_books

@app.get("/books/count", tags=["Inventory"])
def get_books_count():
    return {"total_books": len(db_books), "available": len([b for b in db_books if not b["is_borrowed"]])}

@app.post("/books", status_code=status.HTTP_201_CREATED, tags=["Inventory"])
def add_book(book: BookCreate):
    new_id = max([b["id"] for b in db_books]) + 1 if db_books else 1
    new_book = {**book.dict(), "id": new_id, "is_borrowed": False, "borrower_name": None}
    db_books.append(new_book)
    return new_book


@app.get("/books/{book_id}", tags=["Inventory"])
def get_book_by_id(book_id: int = Path(..., gt=0)):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", tags=["Inventory"])
def update_book(book_id: int, updated_data: BookCreate):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.update(updated_data.dict())
    return {"message": "Book updated successfully", "book": book}

@app.delete("/books/{book_id}", tags=["Inventory"])
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_books.remove(book)
    return {"message": f"Book {book_id} deleted"}


@app.post("/workflow/borrow/{book_id}", tags=["Workflows"])
def borrow_book(book_id: int, user_name: str):
    book = find_book(book_id)
    if not book or book["is_borrowed"]:
        raise HTTPException(status_code=400, detail="Book unavailable or doesn't exist")
    book["is_borrowed"] = True
    book["borrower_name"] = user_name
    return {"status": "Borrowed", "book": book["title"], "to": user_name}

@app.post("/workflow/return/{book_id}", tags=["Workflows"])
def return_book(book_id: int):
    book = find_book(book_id)
    if not book or not book["is_borrowed"]:
        raise HTTPException(status_code=400, detail="Book was not borrowed")
    book["is_borrowed"] = False
    book["borrower_name"] = None
    return {"status": "Returned", "book": book["title"]}


@app.get("/books/search/", tags=["Advanced"])
def search_books(
    q: Optional[str] = Query(None, description="Search by title or author"),
    category: Optional[str] = None,
    sort_by: str = "title",
    page: int = 1,
    limit: int = 5
):
    results = db_books
    
    # Logic for Search & Filtering
    if q:
        results = [b for b in results if q.lower() in b["title"].lower() or q.lower() in b["author"].lower()]
    if category:
        results = [b for b in results if b["category"].lower() == category.lower()]
    
    # Sorting
    results = sorted(results, key=lambda x: x.get(sort_by, "title"))
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "page": page,
        "limit": limit,
        "total_results": len(results),
        "data": results[start:end]
    }

@app.get("/books/available", tags=["Inventory"])
def list_available(): return [b for b in db_books if not b["is_borrowed"]]

@app.patch("/books/{book_id}/status", tags=["Inventory"])
def toggle_status(book_id: int):
    book = find_book(book_id)
    book["is_borrowed"] = not book["is_borrowed"]
    return book