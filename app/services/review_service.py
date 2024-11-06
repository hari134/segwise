from datetime import datetime, timedelta
from google_play_scraper import Sort, reviews
from sqlalchemy import func
from app.utils import classify_review

from app.extensions import db
from app.models import Review


def fetch_reviews(app_id, date, category):
    """
    Fetches reviews for a specific app_id, date, and category, along with the count
    of reviews for that category over the 7 days prior to the selected date.

    Parameters:
    - app_id (str): The app ID for which to fetch reviews.
    - date (str or datetime.date): The specific date for the reviews (string in 'YYYY-MM-DD' format or datetime.date).
    - category (str): The category of reviews to fetch.

    Returns:
    - dict: A dictionary containing:
      - 'reviews': A list of reviews for the specified date and category.
      - 'trend_counts': A list of dictionaries with 'date' and 'count' for each of the past 7 days up to the selected date.
    """

    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD' format.")

    reviews = (
        db.session.query(Review)
        .filter_by(app_id=app_id, review_date=date, category=category)
        .order_by(Review.review_date)
        .all()
    )
    review_list = [
        {
            "user": r.user_name,
            "content": r.content,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in reviews
    ]

    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=8)

    trend_counts_query = (
        db.session.query(Review.review_date, func.count(Review.id).label("count"))
        .filter(
            Review.app_id == app_id,
            Review.category == category,
            Review.review_date >= start_date,
            Review.review_date <= end_date,
        )
        .group_by(Review.review_date)
        .order_by(Review.review_date)
    )

    trend_counts = [
        {"date": day.review_date.isoformat(), "count": day.count}
        for day in trend_counts_query
    ]

    return {"reviews": review_list, "trend_counts": trend_counts}


def scrape_and_store_reviews(app, app_id):
    """
    Scrape Google Play reviews for the given app ID, classify each review, and store the results in the database.

    Parameters:
    app (Flask): The Flask app instance.
    app_id (str): The Google Play app ID for which to fetch and classify reviews.
    """

    with app.app_context():
        print("Scraping started")
        today = datetime.now().date()
        start_date = today - timedelta(days=7)

        review_data, continuation_token = reviews(app_id, count=100, sort=Sort.NEWEST)

        with db.session.no_autoflush:
            for review in review_data:
                review_date = review["at"].date()
                if review_date >= start_date:
                    review_id = review["reviewId"]

                    existing_review = Review.query.filter_by(
                        review_id=review_id
                    ).first()

                    if not existing_review:
                        category = classify_review(review["content"])
                        db_review = Review(
                            app_id=app_id,
                            review_id=review_id,
                            user_name=review["userName"],
                            content=review["content"],
                            category=category,
                            review_date=review_date,
                            timestamp=review["at"],
                        )
                        db.session.add(db_review)

            while continuation_token:
                more_reviews, continuation_token = reviews(
                    app_id,
                    continuation_token=continuation_token,
                    count=100,
                    sort=Sort.NEWEST,
                )
                found_within_date_range = False

                for review in more_reviews:
                    review_date = review["at"].date()
                    if review_date >= start_date:
                        found_within_date_range = True
                        review_id = review["reviewId"]
                        existing_review = Review.query.filter_by(
                            review_id=review_id
                        ).first()
                        if not existing_review:
                            category = classify_review(review["content"])
                            db_review = Review(
                                app_id=app_id,
                                review_id=review_id,
                                user_name=review["userName"],
                                content=review["content"],
                                category=category,
                                review_date=review_date,
                                timestamp=review["at"],
                            )
                            db.session.add(db_review)

                if not found_within_date_range:
                    break

            db.session.commit()
        print(f"Classified reviews saved in the database for app_id {app_id}")
