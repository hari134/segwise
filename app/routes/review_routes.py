from flask import Blueprint, render_template
from app.controllers.review_controller import get_reviews

review_bp = Blueprint("review_bp", __name__)

@review_bp.route("/reviews", methods=["GET"])
def reviews():
    return get_reviews()


@review_bp.route("/")
def home():
    return render_template("reviews.html")  
