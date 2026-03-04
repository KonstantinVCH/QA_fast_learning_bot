"""QA Bot v3.0 — entry point."""
import os
import sys
import logging
from telegram.ext import Application
from .handlers import build_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        logger.error("No BOT_TOKEN found in environment!")
        sys.exit(1)
    groq = os.environ.get("GROQ_API_KEY", "")
    or_key = os.environ.get("OPENROUTER_API_KEY", "")
    print(f"Starting QA Bot v3.0 | Groq={'YES' if groq else 'NO'} | OR={'YES' if or_key else 'NO'}")
    app = build_app(token)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
