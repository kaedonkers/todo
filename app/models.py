# ---
# created: 13 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Define models for data and actions on the database

from datetime import datetime

import pydantic
import sqlalchemy as sqla

from . import database

class Todo(database.BaseDB):
    '''
    Basic todo item model
    '''
    __tablename__ = "todos"
    id = sqla.Column(sqla.Integer, primary_key=True, index=True)
    title = sqla.Column(sqla.String)
    description = sqla.Column(sqla.String, nullable=True)
    completed = sqla.Column(sqla.Boolean, default=False)
    created_at = sqla.Column(
        sqla.DateTime, 
        default=datetime.now, 
        server_default=sqla.func.now(),
        )

class TodoCreate(pydantic.BaseModel):
    '''
    Model for creating a todo item
    '''
    title: str
    description: str = None
    completed: bool = False

class TodoResponse(TodoCreate):
    '''
    Model for returning a todo item
    '''
    id: int
    created_at: datetime
    class ConfigDict:
        from_attributes: True

class TodoUpdate(pydantic.BaseModel):
    '''
    Model for partial update of todo item
    '''
    title: str | None = None
    description: str | None = None
    completed: bool | None = None