import os

# Configuration class for the application

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'devsecret123')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///EclipseSoftwareHelpDesk.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SECRET_KEY = os.getenv('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
