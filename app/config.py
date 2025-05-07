# config.py

# A variable to store the currently logged-in user's username
username = "JesusHdzzzz"
user_id = 22

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', "dev_key")
    DATABASE = os.getenv('DATABASE', "database.db")