from pydantic import BaseModel
from typing import Optional

# Base schema (shared properties)
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

# Schema for creating a new task
class TaskCreate(TaskBase):
    pass

# Schema for reading tasks (includes DB fields)
class TaskRead(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True  # allows SQLAlchemy models to be returned directly

