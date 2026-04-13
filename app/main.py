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
    '''
    Create a new todo item
    '''
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Read
@app.get("/todos", response_model=list[models.TodoResponse])
def read_todos(db: Session = Depends(database.get_db)):
    '''
    Retrieve all todo items
    '''
    return db.query(models.Todo).all()

@app.get("/todos/{todo_id}", response_model=models.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(database.get_db)):
    '''
    Retrieve a single todo item by ID
    '''
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update
@app.patch("/todos/{todo_id}", response_model=models.TodoResponse)
def update_todo(todo_id: int, todo: models.TodoUpdate, db: Session = Depends(database.get_db)):
    '''
    Update some or all fields of a todo item
    '''
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Delete
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    '''
    Delete a todo item
    '''
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"} 
