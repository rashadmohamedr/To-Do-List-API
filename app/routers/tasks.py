from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.dependencies import get_db
from app.schemas.task import TaskCreate, TaskRead
from app.services.task_service import toggle_task, list_tasks, create_task, delete_task

router = APIRouter(prefix="/tasks", tags=["tasks"])
# TASKS CRUD OPERATIONS

# CREATE
@router.post("/Tasks/", response_model=TaskRead)
def createTask(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(task=task,db=db)

## READ
@router.get("/Tasks/", response_model=List[TaskRead])
def listTasks(db: Session = Depends(get_db)):
    """List all tasks"""
    return list_tasks(db=db)

## UPDATE (toggle complete)
@router.post("/Tasks/{task_title}/toggle", response_class=JSONResponse)
def toggleTask(task_title: str, db: Session = Depends(get_db)):
    return toggle_task(task_title=task_title, db=db)

## DELETE
@router.delete("/Tasks/{task_title}", response_class=JSONResponse)
def deleteTask(task_title: str, db: Session = Depends(get_db)):
    return delete_task(task_title=task_title, db=db)