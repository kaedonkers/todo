# ---
# created: 13 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Defining endpoints for API

import sqlalchemy as sqla
import sqlalchemy.orm
import fastapi as fapi

from . import database, models

# Initialize database, ensuring tables are created
database.BaseDB.metadata.create_all(bind=database.engine)

# Initialize API
app = fapi.FastAPI(
    title="todo API",
    description="A simple API for managing todo items, built with FastAPI and SQLite",
    version="1.0.0",    
)

# Create
@app.post("/todos", response_model=models.TodoResponse)
def create_single_todo(todo: models.TodoCreate, db: sqla.orm.Session = fapi.Depends(database.get_db)):
    '''
    Create a new todo item
    '''
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Read
@app.get("/todos", response_model=list[models.TodoResponse])
def read_all_todos(db: sqla.orm.Session = fapi.Depends(database.get_db)):
    '''
    Retrieve all todo items
    '''
    return db.query(models.Todo).all()

@app.get("/todos/{todo_id}", response_model=models.TodoResponse)
def read_single_todo(todo_id: int, db: sqla.orm.Session = fapi.Depends(database.get_db)):
    '''
    Retrieve a single todo item by ID
    '''
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise fapi.HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update
@app.patch("/todos/{todo_id}", response_model=models.TodoResponse)
def update_single_todo(todo_id: int, todo: models.TodoUpdate, db: sqla.orm.Session = fapi.Depends(database.get_db)):
    '''
    Update fields of a single todo item by ID
    '''
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise fapi.HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Delete
@app.delete("/todos/{todo_id}")
def delete_single_todo(todo_id: int, db: sqla.orm.Session = fapi.Depends(database.get_db)):
    '''
    Delete a todo item by ID
    '''
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise fapi.HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"} 

@app.delete("/todos/")
def delete_all_todos(db: sqla.orm.Session = fapi.Depends(database.get_db)):
    '''
    Delete all todo items
    '''
    db.query(models.Todo).delete(synchronize_session=False)
    db.commit()
    return {"message": "All todos deleted successfully"} 

# Additional endpoints for filtering and sorting using query parameters could be added
