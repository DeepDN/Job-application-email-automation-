import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key-change-this'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
