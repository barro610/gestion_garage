# /app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'API_REST'
    SQLALCHEMY_DATABASE_URI = 'postgresql://barro:QFrJzJNxWRH274UxMLMm4zHxC0PZV2qO@dpg-cvp881s9c44c73bvale0-a.oregon-postgres.render.com/chat_platform'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
