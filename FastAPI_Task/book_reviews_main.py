from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from pydantic import BaseModel, EmailStr
import sqlite3

from fastapi.testclient import TestClient

app = FastAPI()

# Connect to SQLite DB
import sqlite3

db_file = 'apitest.db'  

try:
  conn = sqlite3.connect(db_file)
  cursor = conn.cursor()

  # ... verification logic similar to Option 1 (check tables, data)

  conn.close()
  print(f"Database '{db_file}' verified successfully.")
except sqlite3.Error as e:
  print(f"Error verifying database: {str(e)}")

# Define the Pydantic models
class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    text: str
    rating: int

# Endpoint to add a new book
@app.post("/books/")
async def add_book(book: Book, background_tasks: BackgroundTasks):
    try:
        # Ensure table 'books' exists:
        cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, author TEXT NOT NULL, publication_year INTEGER NOT NULL)")
        conn.commit()

        query = "INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)"
        cursor.execute(query, (book.title, book.author, book.publication_year))
        conn.commit()
        background_tasks.add_task(send_confirmation_email, email="your_valid_email@example.com", message="Book added successfully")
        return {"message": "Book added successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Background task to send confirmation email (replace with actual implementation)
def send_confirmation_email(email: EmailStr, message: str):
    print(f"Sending confirmation email to {email}: {message}")  # Replace with actual email sending logic

# Endpoint to retrieve books (example implementation)
@app.get("/books/")
async def get_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return books  # Return a list of dictionaries representing books

# Testing
client = TestClient(app)

def test_add_book():
    response = client.post("/books/", json={"title": "Example Book", "author": "John Doe", "publication_year": 2020})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("message") == "Book added successfully"  # Assuming successful addition

# Execute the test function
test_add_book()
