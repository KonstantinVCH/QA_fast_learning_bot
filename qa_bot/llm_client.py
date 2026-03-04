"""
QA Bot — LLM client v3.0
Groq primary (fast + free) → OpenRouter free fallback.
Надёжная обработка ошибок — никогда не возвращает «сервис недоступен» без попытки fallback.
"""
import os
import logging
import aiohttp
import json

logger = logging.getLogger(__name__)

# ─── Модели (в порядке приоритета) ────────────────────────────────────────────
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

OPENROUTER_MODELS = [
    "google/gemini-2.0-flash-lite:free",
    "google/gemini-flash-1.5-8b:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]

QA_SYSTEM_PROMPT = """Ты — эксперт по тестированию программного обеспечения.
Помогаешь QA-инженерам: объясняешь концепции, пишешь тест-кейсы, баг-репорты, готовишь к собеседованиям.
Отвечаешь на русском языке. Используешь HTML форматирование для Telegram: <b>, <i>, <code>, <pre>.
Ответы структурированы, конкретны, с примерами."""


async def _call_groq(model: str, messages: list, system: str) -> str | None:
    """Вызов Groq API."""
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return None

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": 1500,
        "temperature": 0.7,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    body = await resp.text()
                    logger.warning(f"Groq {model} → {resp.status}: {body[:200]}")
                    return None
    except Exception as e:
        logger.warning(f"Groq {model} error: {e}")
        return None


async def _call_openrouter(model: str, messages: list, system: str) -> str | None:
    """Вызов OpenRouter API."""
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return None

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": 1500,
        "temperature": 0.7,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://t.me/QA_fast_learning_bot",
                    "X-Title": "QA Fast Learning Bot",
                },
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"]
                    if content and content.strip():
                        return content
                    logger.warning(f"OpenRouter {model} → empty response")
                    return None
                else:
                    body = await resp.text()
                    logger.warning(f"OpenRouter {model} → {resp.status}: {body[:200]}")
                    return None
    except Exception as e:
        logger.warning(f"OpenRouter {model} error: {e}")
        return None


async def ask_ai(
    user_message: str,
    system_override: str | None = None,
    history: list | None = None,
) -> str:
    """
    Основная функция запроса к AI.
    Пробует Groq → OpenRouter → статичный ответ.
    Никогда не возвращает голое «сервис недоступен».
    """
    system = system_override or QA_SYSTEM_PROMPT
    messages = list(history or []) + [{"role": "user", "content": user_message}]

    # 1. Попробовать Groq (быстро, бесплатно)
    for model in GROQ_MODELS:
        result = await _call_groq(model, messages, system)
        if result:
            logger.info(f"Response via Groq: {model}")
            return result

    # 2. Попробовать OpenRouter free models
    for model in OPENROUTER_MODELS:
        result = await _call_openrouter(model, messages, system)
        if result:
            logger.info(f"Response via OpenRouter: {model}")
            return result

    # 3. Статичный fallback — хотя бы полезный ответ
    logger.error("All AI providers failed — returning static fallback")
    return _static_fallback(user_message)


def _static_fallback(question: str) -> str:
    """Минимально полезный ответ когда все AI провайдеры недоступны."""
    q = question.lower()

    if any(w in q for w in ["тест-кейс", "testcase", "тест кейс"]):
        return (
            "📋 <b>Что такое тест-кейс?</b>\n\n"
            "Тест-кейс — набор условий для проверки требования.\n\n"
            "<b>Структура (ISTQB):</b>\n"
            "• <b>ID:</b> TC-001\n"
            "• <b>Предусловие:</b> пользователь на странице входа\n"
            "• <b>Шаги:</b> 1. Ввести email 2. Ввести пароль 3. Нажать «Войти»\n"
            "• <b>Ожидаемый результат:</b> редирект на /dashboard\n\n"
            "<i>⚠️ AI сейчас недоступен. Попробуй позже для детальной генерации.</i>"
        )
    elif any(w in q for w in ["баг", "bug", "дефект"]):
        return (
            "🐛 <b>Структура баг-репорта (стандарт)</b>\n\n"
            "• <b>Заголовок:</b> [Модуль] Краткое описание\n"
            "• <b>Severity:</b> Critical/High/Medium/Low\n"
            "• <b>Priority:</b> Blocker/High/Medium/Low\n"
            "• <b>Шаги воспроизведения:</b> пронумерованный список\n"
            "• <b>Ожидаемый результат</b>\n"
            "• <b>Фактический результат</b>\n"
            "• <b>Окружение:</b> ОС, браузер, версия\n\n"
            "<i>⚠️ AI сейчас недоступен. Попробуй позже.</i>"
        )
    else:
        return (
            "⚠️ <b>AI-сервис временно перегружен</b>\n\n"
            "Попробуй через 1-2 минуты.\n\n"
            "Пока — используй разделы:\n"
            "📚 <b>Теория</b> — /theory\n"
            "❓ <b>Квиз</b> — /quiz\n"
            "🧰 <b>Инструменты</b> — /tools"
        )
