from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)  # allows SQLAlchemy models to be returned directly

