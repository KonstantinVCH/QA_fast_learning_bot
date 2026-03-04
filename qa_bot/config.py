"""QA Bot — configuration v3.0"""
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("QA_BOT_TOKEN", "")
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
BOT_VERSION: str = "3.0.0"
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

if not BOT_TOKEN:
    raise ValueError("QA_BOT_TOKEN environment variable is required")
