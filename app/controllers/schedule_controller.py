from flask import request, jsonify
from app.services.schedule_service import create_schedule, modify_schedule

def add_schedule():
    data = request.get_json()
    app_id = data.get("app_id")
    scrape_time = data.get("scrape_time")
    result = create_schedule(app_id, scrape_time)
    return jsonify(result)

def update_schedule(app_id):
    data = request.get_json()
    scrape_time = data.get("scrape_time")
    result = modify_schedule(app_id, scrape_time)
    return jsonify(result)
