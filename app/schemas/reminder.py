from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.models.reminder import ReminderChannel


# Base schemas
class ReminderBase(BaseModel):
    """Base reminder schema with common fields."""
    task_id: UUID
    remind_at: datetime
    channel: ReminderChannel


class ReminderCreate(ReminderBase):
    """Schema for creating a new reminder."""
    pass


class ReminderInDB(ReminderBase):
    """Schema for reminder as stored in database."""
    id: UUID
    sent: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Reminder(ReminderInDB):
    """Public reminder schema returned by API."""
    pass

