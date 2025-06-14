# config.py

# A variable to store the currently logged-in user's username
username = None
user_id = None

import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', "dev_key")
    DATABASE = os.getenv('DATABASE', "database.db")