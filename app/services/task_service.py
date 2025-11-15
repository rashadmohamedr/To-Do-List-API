from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(task: TaskCreate, db: Session):
    """Create a new task"""
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def list_tasks(db: Session):
    """List all tasks"""
    return db.query(Task).all()

def toggle_task(task_title: str, db: Session):
    """Mark a task as completed/uncompleted"""
    task = db.query(Task).filter(Task.title == task_title).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return JSONResponse(status_code=200, content={"message": f"Task{task.title} toggled"})

def delete_task(task_title: str, db: Session):
    """Delete a task"""
    task = db.query(Task).filter(Task.title == task_title).first()
    if task:
        db.delete(task)
        db.commit()
        return JSONResponse(status_code=200, content={"message": f"Task {task_title} deleted"})
    else:
        return JSONResponse(status_code=404, content={"error": f"Task not found"})
