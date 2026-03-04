"""QA Bot v3.0 — entry point."""
import logging
from telegram.ext import Application

from .config import BOT_TOKEN, LOG_LEVEL, BOT_VERSION
from .handlers import register_handlers

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=getattr(logging, LOG_LEVEL, logging.INFO),
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(f"Starting QA Fast Learning Bot v{BOT_VERSION}")
    app = Application.builder().token(BOT_TOKEN).build()
    register_handlers(app)
    logger.info("Bot is running. Polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
