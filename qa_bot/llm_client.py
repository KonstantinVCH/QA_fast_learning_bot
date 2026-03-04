"""QA Bot — LLM client v3.1. OpenRouter with current models."""
import json
import os
import urllib.request
import urllib.error
import logging

logger = logging.getLogger(__name__)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Current working models on OpenRouter (March 2026)
MODELS = [
    "qwen/qwen3.5-flash-02-23",       # Fastest, cheap
    "liquid/lfm-2-24b-a2b",           # Ultra cheap
    "google/gemini-3.1-flash-lite-preview",  # Google, good quality
    "bytedance-seed/seed-2.0-mini",   # ByteDance, 256k context
]


def ask_ai(system_prompt: str, user_message: str, max_tokens: int = 800) -> str:
    """Ask AI with fallback through multiple models."""
    if not OPENROUTER_KEY:
        logger.warning("No OPENROUTER_API_KEY set")
        return ""

    for model in MODELS:
        try:
            payload = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }).encode("utf-8")

            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=payload,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://t.me/QA_fast_learning_bot",
                    "X-Title": "QA Fast Learning Bot"
                }
            )
            resp = urllib.request.urlopen(req, timeout=30)
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"].strip()
            if content:
                logger.info(f"AI response from {model}: {len(content)} chars")
                return content
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            logger.warning(f"Model {model} HTTP {e.code}: {body[:200]}")
        except Exception as e:
            logger.warning(f"Model {model} error: {e}")

    logger.error("All AI models failed")
    return ""

