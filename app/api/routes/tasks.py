from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud import task as crud_task
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.models.task import TaskStatus

router = APIRouter()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db)
) -> Task:
    """
    Create a new task.

    Args:
        task_in: Task creation data
        db: Database session

    Returns:
        Created task
    """
    task = await crud_task.create_task(db=db, task_in=task_in)
    return task


@router.get("/", response_model=List[Task])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: TaskStatus | None = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[Task]:
    """
    Retrieve tasks with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Optional status filter
        db: Database session

    Returns:
        List of tasks
    """
    tasks = await crud_task.get_tasks(
        db=db,
        skip=skip,
        limit=limit,
        status=status
    )
    return list(tasks)


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Task:
    """
    Retrieve a specific task by ID.

    Args:
        task_id: Task UUID
        db: Database session

    Returns:
        Task details

    Raises:
        HTTPException: 404 if task not found
    """
    task = await crud_task.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db)
) -> Task:
    """
    Update an existing task.

    Args:
        task_id: Task UUID
        task_update: Task update data
        db: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found
    """
    task = await crud_task.update_task(
        db=db,
        task_id=task_id,
        task_update=task_update
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a task.

    Args:
        task_id: Task UUID
        db: Database session

    Raises:
        HTTPException: 404 if task not found
    """
    deleted = await crud_task.delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

