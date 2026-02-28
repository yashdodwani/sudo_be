from typing import Sequence
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, task_in: TaskCreate) -> Task:
    """
    Create a new task in the database.

    Args:
        db: Async database session
        task_in: Task creation schema

    Returns:
        Created task instance
    """
    db_task = Task(**task_in.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_task(db: AsyncSession, task_id: UUID) -> Task | None:
    """
    Retrieve a task by ID.

    Args:
        db: Async database session
        task_id: Task UUID

    Returns:
        Task instance or None if not found
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    return result.scalar_one_or_none()


async def get_tasks(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: TaskStatus | None = None
) -> Sequence[Task]:
    """
    Retrieve multiple tasks with optional filtering.

    Args:
        db: Async database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Optional status filter

    Returns:
        List of task instances
    """
    query = select(Task)

    if status:
        query = query.where(Task.status == status)

    query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()


async def update_task(
    db: AsyncSession,
    task_id: UUID,
    task_update: TaskUpdate
) -> Task | None:
    """
    Update an existing task.

    Args:
        db: Async database session
        task_id: Task UUID
        task_update: Task update schema with fields to update

    Returns:
        Updated task instance or None if not found
    """
    # Get existing task
    db_task = await get_task(db, task_id)
    if not db_task:
        return None

    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_task, field, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: UUID) -> bool:
    """
    Delete a task by ID.

    Args:
        db: Async database session
        task_id: Task UUID

    Returns:
        True if task was deleted, False if not found
    """
    db_task = await get_task(db, task_id)
    if not db_task:
        return False

    await db.delete(db_task)
    await db.commit()
    return True

