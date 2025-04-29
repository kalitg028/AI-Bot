import os
from typing import List

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN = int(os.getenv("ADMIN", ""))

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", ""))

DB_URI = os.getenv("DB_URI", "")
DB_NAME = os.getenv("DB_NAME", "")

IS_FSUB = bool(os.getenv("FSUB", True)) # Set "True" For Enable Force Subscribe
AUTH_CHANNELS = list(map(int, os.getenv("AUTH_CHANNEL", "-100xxxxxxxxx -100xxxxxxx").split())) # Add Multiple channel id

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
