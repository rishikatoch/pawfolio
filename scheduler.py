import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from app import app
from app.services.reminder_service import send_due_reminders

logging.basicConfig(level=logging.INFO)

scheduler = BlockingScheduler(timezone="Asia/Kolkata")


def run_daily_reminders():
    """
    Runs the daily reminder service.
    """

    with app.app_context():
        logging.info("Starting daily reminder job...")

        try:
            send_due_reminders()
            logging.info("Daily reminder job completed successfully.")

        except Exception:
            logging.exception("Reminder job failed.")


scheduler.add_job(
    func=run_daily_reminders,
    trigger="cron",
    hour=9,
    minute=0,
    id="daily_reminders",
    replace_existing=True,
)

if __name__ == "__main__":
    logging.info("Starting Pawfolio Reminder Scheduler...")
    scheduler.start()
