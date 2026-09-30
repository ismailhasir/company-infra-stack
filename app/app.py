from fastapi import FastAPI,status
from pydantic import BaseModel

app = FastAPI()

notes_list = []


#1 Define the data model for the note
class Note(BaseModel):
    text: str


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}   

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/notes", status_code=status.HTTP_201_CREATED, response_model=Note)
async def create_note(note: Note):
    notes_list.append(note)
    return note

@app.get("/notes")
async def read_notes():
    return notes_list

