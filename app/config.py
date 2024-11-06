import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/segwise_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
