from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud import reminder as crud_reminder
from app.crud import task as crud_task
from app.schemas.reminder import Reminder, ReminderCreate

router = APIRouter()


@router.post("/", response_model=Reminder, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    reminder_in: ReminderCreate,
    db: AsyncSession = Depends(get_db)
) -> Reminder:
    """
    Create a new reminder.

    Args:
        reminder_in: Reminder creation data
        db: Database session

    Returns:
        Created reminder

    Raises:
        HTTPException: 404 if associated task not found
    """
    # Verify task exists
    task = await crud_task.get_task(db=db, task_id=reminder_in.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {reminder_in.task_id} not found"
        )

    reminder = await crud_reminder.create_reminder(db=db, reminder_in=reminder_in)
    return reminder


@router.get("/", response_model=List[Reminder])
async def get_reminders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    task_id: UUID | None = Query(None),
    sent: bool | None = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[Reminder]:
    """
    Retrieve reminders with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        task_id: Optional task ID filter
        sent: Optional sent status filter
        db: Database session

    Returns:
        List of reminders
    """
    reminders = await crud_reminder.get_reminders(
        db=db,
        skip=skip,
        limit=limit,
        task_id=task_id,
        sent=sent
    )
    return list(reminders)


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(
    reminder_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a reminder.

    Args:
        reminder_id: Reminder UUID
        db: Database session

    Raises:
        HTTPException: 404 if reminder not found
    """
    deleted = await crud_reminder.delete_reminder(db=db, reminder_id=reminder_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reminder with id {reminder_id} not found"
        )

