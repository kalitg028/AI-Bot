import re
from os import environ, getenv

API_ID = environ.get("API_ID", "")
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
OWNER_ID = int(environ.get("OWNER_ID", ""))
DATABASE_URL = environ.get("DATABASE_URL",  "")
DATABASE_NAME = environ.get("DATABASE_NAME", "ai")
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", ""))
AUTH_CHANNEL = int(environ.get("AUTH_CHANNEL", ""))
FSUB = environ.get("FSUB", True)
GOOGLE_API_KEY = environ.get('API_KEY', '')