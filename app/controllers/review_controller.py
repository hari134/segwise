from flask import request, jsonify
from app.services.review_service import fetch_reviews

def get_reviews():
    date = request.args.get("date")
    category = request.args.get("category")
    app_id = request.args.get("app_id")

    reviews = fetch_reviews(app_id, date, category)
    return jsonify(reviews)
