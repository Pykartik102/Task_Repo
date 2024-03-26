from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from pydantic import BaseModel, EmailStr
import mysql.connector
from fastapi.testclient import TestClient

app = FastAPI()

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='',
    password='',
    database='apitest'
)
cursor = conn.cursor()

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
async def get_books():
    # Implementation to retrieve books goes here
    pass

async def add_book(book: Book, background_tasks: BackgroundTasks):
    try:
        query = "INSERT INTO books (title, author, publication_year) VALUES (%s, %s, %s)"
        values = (book.title, book.author, book.publication_year)
        cursor.execute(query, values)
        conn.commit()
        background_tasks.add_task(send_confirmation_email, email="kartikdev102@gmail.com", message="Book added successfully")
        return {"message": "Book added successfully"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error adding book: {str(e)}")

# Background task to send confirmation email
def send_confirmation_email(email: EmailStr, message: str):
    print(f"Sending confirmation email to {email}: {message}")

# Testing
client = TestClient(app)

def test_add_book():
    response = client.post("/books/", json={"title": "Example Book", "author": "John Doe", "publication_year": 2020})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Book added successfully"}

# Execute the test function
test_add_book()
