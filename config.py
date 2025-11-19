import os

class Config:
    # Use environment variables if set, otherwise fallback to defaults
    SECRET_KEY = os.getenv('SECRET_KEY', 'devsecret123')
    
    # If DATABASE_URL is set (for Docker), use it
    # Otherwise, fallback to a local SQLite file
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///EclipseSoftwareHelpDesk.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
