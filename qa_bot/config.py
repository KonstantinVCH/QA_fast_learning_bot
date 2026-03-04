"""QA Bot — configuration v2.0"""
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("QA_BOT_TOKEN", "")
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
BOT_VERSION: str = "2.1.0"
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

if not BOT_TOKEN:
    raise ValueError("QA_BOT_TOKEN environment variable is required")
