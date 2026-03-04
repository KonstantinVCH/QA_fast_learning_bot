#!/usr/bin/env python3
"""QA Bot v3.0 - entry point."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    from .handlers import build_app
    token = os.getenv("QA_BOT_TOKEN", "")
    if not token:
        print("ERROR: QA_BOT_TOKEN not set!", file=sys.stderr)
        sys.exit(1)
    
    groq_key = os.getenv("GROQ_API_KEY", "")
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    print(f"Starting QA Bot v3.0 | Groq={'YES' if groq_key else 'NO'} | OR={'YES' if openrouter_key else 'NO'}")
    
    app = build_app(token)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
