"""QA Bot — LLM client v3.2. Async OpenRouter with fallback models."""
import json
import os
import asyncio
import urllib.request
import urllib.error
import logging

logger = logging.getLogger(__name__)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Current working models on OpenRouter (March 2026)
MODELS = [
    "qwen/qwen3.5-flash-02-23",
    "liquid/lfm-2-24b-a2b",
    "google/gemini-3.1-flash-lite-preview",
    "bytedance-seed/seed-2.0-mini",
]


def _ask_ai_sync(system_prompt: str, user_message: str, max_tokens: int = 800) -> str:
    """Synchronous AI call with fallback through multiple models."""
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


async def ask_ai(system_prompt: str, user_message: str = "", max_tokens: int = 800) -> str:
    """Async AI call. Accepts (system, user) or (user_only) for backward compat."""
    if not user_message:
        # Called with single arg: ask_ai(text) - use as user message
        user_message = system_prompt
        system_prompt = "Ты опытный QA-инженер. Отвечай кратко, по делу, на русском языке."
    
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _ask_ai_sync, system_prompt, user_message, max_tokens)
