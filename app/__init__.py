from flask import Flask
from .config import config  # Import your configuration settings
from .extensions import db, migrate  # Import db and migrate from extensions
from .tasks.scheduler import init_scheduler  # Import the scheduler initializer
from .routes import all_blueprints# Import the routes blueprint

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # Load configuration based on environment

    # Import models to register with SQLAlchemy
    from .models import AppSchedule, Review
    print(config[config_name].SQLALCHEMY_DATABASE_URI)

    # Initialize SQLAlchemy and Migrate with the app instance
    db.init_app(app)
    migrate.init_app(app, db)

    # Register the routes blueprint
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    # Initialize the scheduler with the app context
    init_scheduler(app)

    return app
