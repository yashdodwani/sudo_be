import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.task import Task


class ReminderChannel(str, enum.Enum):
    """Reminder channel enumeration."""
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    UI = "ui"


class Reminder(Base):
    """Reminder model for task notifications."""

    __tablename__ = "reminders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    remind_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )
    channel: Mapped[ReminderChannel] = mapped_column(
        Enum(ReminderChannel, native_enum=False),
        nullable=False
    )
    sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    task: Mapped["Task"] = relationship(
        "Task",
        back_populates="reminders"
    )

    def __repr__(self) -> str:
        return f"<Reminder(id={self.id}, task_id={self.task_id}, remind_at={self.remind_at}, sent={self.sent})>"

