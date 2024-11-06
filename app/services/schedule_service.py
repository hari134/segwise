from app.models import AppSchedule
from app import db
from datetime import datetime
from flask import current_app


def create_schedule(app_id, scrape_time):
    existing_schedule = db.session.query(AppSchedule).filter_by(app_id=app_id).first()
    if existing_schedule:
        return {"error": "Schedule already exists for this app_id"}, 400

    schedule = AppSchedule(
        app_id=app_id, scrape_time=datetime.strptime(scrape_time, "%H:%M:%S").time()
    )
    db.session.add(schedule)
    db.session.commit()
    from app.tasks.scheduler import schedule_scraper_tasks
    return {"message": "Schedule created successfully"}


def modify_schedule(app_id, scrape_time):
    schedule = db.session.query(AppSchedule).filter_by(app_id=app_id).first()
    if not schedule:
        return {"error": "Schedule not found"}, 404

    schedule.scrape_time = datetime.strptime(scrape_time, "%H:%M:%S").time()
    db.session.commit()
    from app.tasks.scheduler import schedule_scraper_tasks
    return {"message": "Schedule updated successfully"}


def get_scheduled_apps():
    """
    Retrieve all scheduled apps and their scrape times from the AppSchedule table.

    Returns:
    list of tuples: A list where each tuple contains an app ID and its corresponding scrape time.
    """
    scheduled_apps = AppSchedule.query.with_entities(AppSchedule.app_id, AppSchedule.scrape_time).all()
    return [(app.app_id, app.scrape_time) for app in scheduled_apps]
