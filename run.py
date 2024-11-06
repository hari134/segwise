from app import create_app, db

from app import create_app, db
from app.models import AppSchedule
from datetime import time

app = create_app()

@app.cli.command("seed_data")
def seed_data():
    """Seed the database with initial data for AppSchedule."""

    existing_schedule = AppSchedule.query.filter_by(app_id="com.superplaystudios.dicedreams").first()
    if existing_schedule:
        print("Seed data for AppSchedule already exists. Skipping seeding.")
        return

    schedule = AppSchedule(
        app_id="com.superplaystudios.dicedreams",
        scrape_time=time(12, 0, 0)
    )

    db.session.add(schedule)
    db.session.commit()
    print("Database seeded with AppSchedule entry for com.superplaystudios.dicedreams.")


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000,use_reloader=False)
