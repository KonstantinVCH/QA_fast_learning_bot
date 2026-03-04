"""QA Bot — LLM client v2.1. OpenRouter with smart model fallback."""
import os
import logging
import aiohttp

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Ты — опытный QA-инженер с 10+ годами опыта.
Помогаешь тестировщикам — от джунов до мидлов — разбираться в профессии.
Отвечаешь строго на русском языке. Используй HTML-форматирование для Telegram:
<b>жирный</b>, <i>курсив</i>, <code>код</code>, <pre>блок кода</pre>.
Отвечай кратко и по делу. Максимум 600 слов. Приводи конкретные примеры.
Ссылайся на ISTQB-стандарты когда уместно."""

# Free models through OpenRouter — ordered by reliability
MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemini-flash-1.5:free",
    "microsoft/phi-4-reasoning:free",
]


async def ask_ai(user_message: str, system_override: str = "") -> str:
    """Call LLM with QA context. Returns response text or user-friendly error."""
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return "❌ OpenRouter API ключ не настроен. Обратитесь к администратору."

    system = system_override or SYSTEM_PROMPT
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    for model in MODELS:
        result = await _try_model(api_key, model, messages)
        if result:
            return result

    return "⚠️ AI-сервис временно недоступен. Попробуйте через пару минут."


async def _try_model(api_key: str, model: str, messages: list) -> str:
    """Try one model up to 2 times. Returns text or empty string."""
    import asyncio
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/KonstantinVCH/QA_fast_learning_bot",
        "X-Title": "QA Fast Learning Bot",
    }
    payload = {"model": model, "messages": messages, "max_tokens": 1000, "temperature": 0.7}
    timeout = aiohttp.ClientTimeout(total=30)

    for attempt in range(2):
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(OPENROUTER_URL, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        text = data["choices"][0]["message"]["content"].strip()
                        if text:
                            return text
                    elif resp.status == 429:
                        logger.warning(f"Rate limit on {model}")
                        return ""
                    else:
                        logger.warning(f"HTTP {resp.status} from {model}")
        except Exception as e:
            logger.warning(f"Model {model} attempt {attempt + 1} error: {e}")
            if attempt == 0:
                await asyncio.sleep(2)

    return ""
