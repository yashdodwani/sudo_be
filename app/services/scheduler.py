import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.crud.reminder import get_pending_reminders

logger = logging.getLogger(__name__)


class ReminderSchedulerService:
    """
    Service for scheduling and processing reminders.

    This service runs periodically to check for pending reminders
    and process them. Currently logs reminders; can be extended
    to integrate with messaging services.
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._is_running = False

    async def process_pending_reminders(self) -> None:
        """
        Check for and process pending reminders.

        Fetches all unsent reminders that are due and logs them.
        In production, this would trigger actual notifications via
        Telegram, WhatsApp, or other channels.
        """
        async with AsyncSessionLocal() as db:
            try:
                current_time = datetime.now(timezone.utc)
                pending_reminders = await get_pending_reminders(
                    db=db,
                    current_time=current_time
                )

                if pending_reminders:
                    logger.info(f"Found {len(pending_reminders)} pending reminder(s)")

                    for reminder in pending_reminders:
                        logger.info(
                            f"Reminder {reminder.id} for task {reminder.task_id} "
                            f"via {reminder.channel.value} - Due at {reminder.remind_at}"
                        )
                        # TODO: Implement actual notification sending
                        # await self._send_notification(reminder)

                        # Mark as sent (uncomment when notifications are implemented)
                        # reminder.sent = True

                    # await db.commit()
                else:
                    logger.debug("No pending reminders found")

            except Exception as e:
                logger.error(f"Error processing reminders: {e}", exc_info=True)
                await db.rollback()

    def start(self) -> None:
        """Start the scheduler service."""
        if not self._is_running:
            # Run every minute
            self.scheduler.add_job(
                self.process_pending_reminders,
                'interval',
                minutes=1,
                id='process_reminders',
                replace_existing=True
            )
            self.scheduler.start()
            self._is_running = True
            logger.info("Reminder scheduler service started")

    def stop(self) -> None:
        """Stop the scheduler service."""
        if self._is_running:
            self.scheduler.shutdown()
            self._is_running = False
            logger.info("Reminder scheduler service stopped")


# Global scheduler instance
reminder_scheduler = ReminderSchedulerService()

