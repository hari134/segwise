from .extensions import db

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String, index=True)
    review_id = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    review_date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class AppSchedule(db.Model):
    __tablename__ = "app_schedule"

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String, unique=True, nullable=False)
    scrape_time = db.Column(db.Time, nullable=False)
