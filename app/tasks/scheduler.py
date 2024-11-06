from apscheduler.schedulers.background import BackgroundScheduler
from app.services.review_service import scrape_and_store_reviews
from app.models import AppSchedule
scheduler = BackgroundScheduler()

def schedule_scraper_tasks(app):
    """Schedules scraping tasks based on AppSchedule entries in the database."""
    with app.app_context():
        schedules = AppSchedule.query.all()
        for schedule in schedules:
            job_id = f"scraper_{schedule.app_id}"
            scheduler.add_job(
                func=scrape_and_store_reviews,
                trigger="cron",
                hour=schedule.scrape_time.hour,
                minute=schedule.scrape_time.minute,
                args=[app, schedule.app_id],  
                id=job_id,
                replace_existing=True
            )

def init_scheduler(app):
    """Initializes and starts the scheduler with the given Flask app context."""
    if not scheduler.running:
        scheduler.app = app
        scheduler.start()
        schedule_scraper_tasks(app)
