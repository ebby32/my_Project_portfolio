import os
from dotenv import load_dotenv

load_dotenv()



class Config:
    SECRET_KEY = 'DEV'

    EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    # SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL','sqlite:///site.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False