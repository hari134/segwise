from flask import Blueprint
from app.controllers.schedule_controller import add_schedule, update_schedule

schedule_bp = Blueprint("schedule_bp", __name__)

@schedule_bp.route("/schedule", methods=["POST"])
def add_scrape_schedule():
    return add_schedule()

@schedule_bp.route("/schedule/<app_id>", methods=["PUT"])
def update_scrape_schedule(app_id):
    return update_schedule(app_id)
