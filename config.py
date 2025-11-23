from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'development-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///EclipseSoftwareHelpDesk.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
