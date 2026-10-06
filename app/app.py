import os
import psycopg
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

def get_connection():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dbname=os.environ["DB_NAME"],
    )


def init_db():
    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id SERIAL PRIMARY KEY, text TEXT NOT NULL)"
        )

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


#1 Define the data model for the note
class Note(BaseModel):
    text: str


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}   

@app.get("/health")
def health_check():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
    except psycopg.Error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database unavailable",
        )
    return {"status": "ok"}

@app.post("/notes", status_code=status.HTTP_201_CREATED, response_model=Note)
def create_note(note: Note):
    with get_connection() as conn:
        conn.execute("INSERT INTO notes (text) VALUES (%s)", (note.text,))
    return note

@app.get("/notes")
def read_notes():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, text FROM notes ORDER BY id").fetchall()
    return [{"id": row[0], "text": row[1]} for row in rows]
