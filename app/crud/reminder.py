from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate


async def create_reminder(db: AsyncSession, reminder_in: ReminderCreate) -> Reminder:
    """
    Create a new reminder in the database.

    Args:
        db: Async database session
        reminder_in: Reminder creation schema

    Returns:
        Created reminder instance
    """
    db_reminder = Reminder(**reminder_in.model_dump())
    db.add(db_reminder)
    await db.commit()
    await db.refresh(db_reminder)
    return db_reminder


async def get_reminder(db: AsyncSession, reminder_id: UUID) -> Reminder | None:
    """
    Retrieve a reminder by ID.

    Args:
        db: Async database session
        reminder_id: Reminder UUID

    Returns:
        Reminder instance or None if not found
    """
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id)
    )
    return result.scalar_one_or_none()


async def get_reminders(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    task_id: UUID | None = None,
    sent: bool | None = None
) -> Sequence[Reminder]:
    """
    Retrieve multiple reminders with optional filtering.

    Args:
        db: Async database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        task_id: Optional task ID filter
        sent: Optional sent status filter

    Returns:
        List of reminder instances
    """
    query = select(Reminder)

    filters = []
    if task_id:
        filters.append(Reminder.task_id == task_id)
    if sent is not None:
        filters.append(Reminder.sent == sent)

    if filters:
        query = query.where(and_(*filters))

    query = query.offset(skip).limit(limit).order_by(Reminder.remind_at.asc())

    result = await db.execute(query)
    return result.scalars().all()


async def get_pending_reminders(
    db: AsyncSession,
    current_time: datetime
) -> Sequence[Reminder]:
    """
    Get all unsent reminders that are due.

    Args:
        db: Async database session
        current_time: Current datetime to check against

    Returns:
        List of pending reminder instances
    """
    result = await db.execute(
        select(Reminder)
        .where(
            and_(
                Reminder.sent == False,
                Reminder.remind_at <= current_time
            )
        )
        .order_by(Reminder.remind_at.asc())
    )
    return result.scalars().all()


async def mark_reminder_sent(db: AsyncSession, reminder_id: UUID) -> Reminder | None:
    """
    Mark a reminder as sent.

    Args:
        db: Async database session
        reminder_id: Reminder UUID

    Returns:
        Updated reminder instance or None if not found
    """
    db_reminder = await get_reminder(db, reminder_id)
    if not db_reminder:
        return None

    db_reminder.sent = True
    await db.commit()
    await db.refresh(db_reminder)
    return db_reminder


async def delete_reminder(db: AsyncSession, reminder_id: UUID) -> bool:
    """
    Delete a reminder by ID.

    Args:
        db: Async database session
        reminder_id: Reminder UUID

    Returns:
        True if reminder was deleted, False if not found
    """
    db_reminder = await get_reminder(db, reminder_id)
    if not db_reminder:
        return False

    await db.delete(db_reminder)
    await db.commit()
    return True

