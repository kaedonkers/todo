# ---
# created: 13 Apr 2026
# author: kaedonkers
# modified: 13 Apr 2026
# ---
# Defining endpoints for API

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from . import database, models

# Initialize database, ensuring tables are created
database.BaseDB.metadata.create_all(bind=database.engine)

# Initialize API
app = FastAPI()

# Create
@app.post("/todos", response_model=models.TodoResponse)
def create_todo(todo: models.TodoCreate, db: Session = Depends(database.get_db)):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Read
@app.get("/todos", response_model=list[models.TodoResponse])
def read_todos(db: Session = Depends(database.get_db)):
    return db.query(models.Todo).all()
