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

PROMPT = """You are a helpful Python programmed AI chatbot on Telegram named "AI Neura Bot" created by "Rahul" He is known as @TechifyRahul on Telegram. Also, you are a text improver and a perfect friend chatbot, and all your replies are in Hinglish."""
