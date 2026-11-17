
from fastapi import APIRouter, Depends, HTTPException, status , Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import get_db
from models import Task, User
from schemas import TaskCreate, TaskUpdate, TaskResponse
from routers.auth import get_current_user
from logger import  logger
# logger.info("task created successfulyy")
# logger.warning("task not found")
# logger.error("darabase operation faild")

router = APIRouter(prefix="/tasks", tags=["tasks"])


# CREATE TASK
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception:
        db.rollback()
        raise    

    return new_task


# GET ALL TASKS
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.scalars(
        select(Task).where(
            Task.user_id == current_user.id
        )
    ).all()

    return tasks


# GET TASK BY ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# UPDATE TASK
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# DELETE TASK
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }



@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    try:
        for key, value in update_data.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        logger.exception("Failed to update task")

        raise HTTPException(
            status_code=500,
            detail="Failed to update task"
        )



@router.get("/page/",response_model=list[TaskResponse])
def get_paginate_tasks(
    skip: int = Query(default=0 , ge=0),
    limit: int = Query(default=10 , ge= 1, le = 100),
    db : Session=Depends(get_db),
    current_user : User=Depends(get_current_user)
):
    tasks = db.scalars(
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.id)
        .offset(skip)
        .limit(limit)
    ).all()

    return tasks        
@router.get("/filter/",response_model=list[TaskResponse])
def filter_tasks(completed:bool,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    tasks = db.scalars(select(Task).where(Task.user_id == current_user.id,Task.completed == completed)).all()

    return tasks
    