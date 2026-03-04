"""QA Bot — Telegram handlers v2.1. Inline keyboards, rich UX."""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes,
)
from .llm_client import ask_ai
from .quiz import QuizSession, QUIZ_BANK

logger = logging.getLogger(__name__)

# Welcome banner (public domain QA-themed image)
WELCOME_IMAGE = "https://i.imgur.com/2nCt3Sbl.jpg"

# ═══════════════════════════════════════════════════════════
# KEYBOARDS
# ═══════════════════════════════════════════════════════════

def kb_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧪 Тест-кейсы", callback_data="menu_testcase"),
         InlineKeyboardButton("🐛 Баг-репорт", callback_data="menu_bugreport")],
        [InlineKeyboardButton("❓ Квиз ISTQB", callback_data="menu_quiz"),
         InlineKeyboardButton("📚 Теория", callback_data="menu_theory")],
        [InlineKeyboardButton("🧰 Инструменты", callback_data="menu_tools"),
         InlineKeyboardButton("💼 Собеседование", callback_data="menu_interview")],
        [InlineKeyboardButton("💬 Спросить AI", callback_data="menu_ask")],
    ])


def kb_quiz_levels() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Лёгкий", callback_data="quiz_easy"),
         InlineKeyboardButton("🟡 Средний", callback_data="quiz_medium")],
        [InlineKeyboardButton("🔴 Сложный", callback_data="quiz_hard"),
         InlineKeyboardButton("🎲 Микс", callback_data="quiz_mixed")],
        [InlineKeyboardButton("⬅️ Меню", callback_data="menu_main")],
    ])


def kb_theory_topics() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📐 Техники тест-дизайна", callback_data="theory_design"),
         InlineKeyboardButton("🔬 Уровни тестирования", callback_data="theory_levels")],
        [InlineKeyboardButton("⚡ Виды тестирования", callback_data="theory_types"),
         InlineKeyboardButton("📋 ISTQB принципы", callback_data="theory_principles")],
        [InlineKeyboardButton("🤖 Автоматизация", callback_data="theory_automation"),
         InlineKeyboardButton("📱 Mobile тестирование", callback_data="theory_mobile")],
        [InlineKeyboardButton("⬅️ Меню", callback_data="menu_main")],
    ])


def kb_back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="menu_main")]
    ])


# ═══════════════════════════════════════════════════════════
# WELCOME TEXT
# ═══════════════════════════════════════════════════════════

WELCOME_TEXT = (
    "👋 <b>Привет! Я QA Fast Learning Bot</b> 🎓\n\n"
    "Твой персональный помощник в мире тестирования.\n"
    "Я обучаю по программе <b>ISTQB CTFL v4.0</b> и помогаю с реальными задачами.\n\n"
    "Выбери раздел:"
)

# ═══════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_photo(
            photo=WELCOME_IMAGE,
            caption=WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=kb_main_menu(),
        )
    except Exception:
        await update.message.reply_text(
            WELCOME_TEXT, parse_mode="HTML", reply_markup=kb_main_menu()
        )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📖 <b>Доступные команды:</b>\n\n"
        "/start — главное меню\n"
        "/testcase — генерация тест-кейсов\n"
        "/bugreport — оформить баг-репорт\n"
        "/quiz — квиз по ISTQB\n"
        "/theory — теория тестирования\n"
        "/tools — инструменты QA\n"
        "/interview — подготовка к собеседованию\n"
        "/ask — задать вопрос AI\n\n"
        "<i>Или просто напиши вопрос — я отвечу!</i>"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_testcase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "testcase"
    text = (
        "🧪 <b>Генерация тест-кейсов</b>\n\n"
        "Опиши функциональность — я создам тест-кейсы по ISTQB-стандарту.\n\n"
        "<i>Пример:</i>\n"
        "«Форма входа: поля email и пароль. Email должен существовать в базе. "
        "После 5 неверных попыток — блокировка на 15 минут.»"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_bugreport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "bugreport"
    text = (
        "🐛 <b>Оформление баг-репорта</b>\n\n"
        "Опиши баг — я оформлю его по стандарту.\n\n"
        "<i>Пример:</i>\n"
        "«При вводе пароля из 7 символов система принимает его, "
        "хотя должна требовать минимум 8.»"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"❓ <b>Квиз по ISTQB</b>\n\n"
        f"База: {len(QUIZ_BANK)} вопросов из официальных программ ISTQB.\n"
        "Выбери уровень сложности:"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_quiz_levels())


async def cmd_theory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📚 <b>Теория тестирования</b>\n\nВыбери тему:",
        parse_mode="HTML",
        reply_markup=kb_theory_topics(),
    )


async def cmd_tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_tools(update.message.reply_text)


async def cmd_interview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "interview"
    text = (
        "💼 <b>Подготовка к собеседованию</b>\n\n"
        "Задай тему — и я дам типичные вопросы с ответами.\n\n"
        "Например:\n"
        "• «Вопросы по теории тестирования»\n"
        "• «API тестирование на собеседовании»\n"
        "• «Как ответить на вопрос о приоритизации багов»"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "ask"
    await update.message.reply_text(
        "💬 <b>Спроси AI-эксперта</b>\n\nЗадай любой вопрос по QA:",
        parse_mode="HTML",
        reply_markup=kb_back_to_menu(),
    )


# ═══════════════════════════════════════════════════════════
# CALLBACK HANDLER
# ═══════════════════════════════════════════════════════════

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # Main menu navigation
    if data == "menu_main":
        await query.message.edit_text(
            WELCOME_TEXT, parse_mode="HTML", reply_markup=kb_main_menu()
        )
    elif data == "menu_testcase":
        context.user_data["mode"] = "testcase"
        await query.message.edit_text(
            "🧪 <b>Генерация тест-кейсов</b>\n\nОпиши функциональность:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )
    elif data == "menu_bugreport":
        context.user_data["mode"] = "bugreport"
        await query.message.edit_text(
            "🐛 <b>Оформление баг-репорта</b>\n\nОпиши проблему:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )
    elif data == "menu_quiz":
        await query.message.edit_text(
            f"❓ <b>Квиз по ISTQB</b>\n\nБаза: {len(QUIZ_BANK)} вопросов. Выбери уровень:",
            parse_mode="HTML", reply_markup=kb_quiz_levels()
        )
    elif data == "menu_theory":
        await query.message.edit_text(
            "📚 <b>Теория тестирования</b>\n\nВыбери тему:",
            parse_mode="HTML", reply_markup=kb_theory_topics()
        )
    elif data == "menu_tools":
        await _send_tools(
            lambda t, **kw: query.message.edit_text(t, **kw)
        )
    elif data == "menu_interview":
        context.user_data["mode"] = "interview"
        await query.message.edit_text(
            "💼 <b>Собеседование</b>\n\nНапиши тему — дам вопросы и ответы:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )
    elif data == "menu_ask":
        context.user_data["mode"] = "ask"
        await query.message.edit_text(
            "💬 <b>AI-эксперт</b>\n\nЗадай любой вопрос по QA:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )

    # Quiz level selection
    elif data.startswith("quiz_"):
        level = data[5:]  # easy / medium / hard / mixed
        session = QuizSession(level=level)
        context.user_data["quiz"] = session
        context.user_data["mode"] = "quiz"
        await query.message.edit_text(
            session.current_question(),
            parse_mode="HTML",
            reply_markup=kb_back_to_menu(),
        )

    # Theory topics
    elif data.startswith("theory_"):
        topic = data[7:]
        await query.message.edit_text("⏳ Загружаю теорию...", parse_mode="HTML")
        content = await _get_theory(topic)
        await query.message.edit_text(
            content, parse_mode="HTML", reply_markup=kb_theory_topics(),
            disable_web_page_preview=True
        )


# ═══════════════════════════════════════════════════════════
# MESSAGE HANDLER
# ═══════════════════════════════════════════════════════════

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    mode = context.user_data.get("mode", "ask")

    # Quiz
    if mode == "quiz":
        session: QuizSession | None = context.user_data.get("quiz")
        if session and not session.is_finished:
            response = session.answer(text)
            kb = None if session.is_finished else kb_back_to_menu()
            if session.is_finished:
                context.user_data.pop("mode", None)
                context.user_data.pop("quiz", None)
            await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb)
            return

    # Testcase
    if mode == "testcase":
        msg = await update.message.reply_text("⏳ Генерирую тест-кейсы по ISTQB...")
        response = await ask_ai(
            f"Напиши подробные тест-кейсы по ISTQB-стандарту для:\n\n{text}",
            system_override=_TESTCASE_SYSTEM,
        )
        context.user_data.pop("mode", None)
        await msg.delete()
        await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())
        return

    # Bugreport
    if mode == "bugreport":
        msg = await update.message.reply_text("⏳ Оформляю баг-репорт...")
        response = await ask_ai(
            f"Оформи баг-репорт по стандарту:\n\n{text}",
            system_override=_BUGREPORT_SYSTEM,
        )
        context.user_data.pop("mode", None)
        await msg.delete()
        await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())
        return

    # Interview
    if mode == "interview":
        msg = await update.message.reply_text("⏳ Готовлю вопросы для собеседования...")
        response = await ask_ai(
            f"Дай топ-5 вопросов на собеседовании по теме «{text}» с развёрнутыми ответами.",
        )
        context.user_data.pop("mode", None)
        await msg.delete()
        await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())
        return

    # Default: general QA question
    msg = await update.message.reply_text("🤔 Думаю...")
    response = await ask_ai(text)
    await msg.delete()
    await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

_TESTCASE_SYSTEM = """Ты — QA-инженер. Пишешь тест-кейсы по ISTQB-стандарту в HTML для Telegram.

Формат каждого тест-кейса (HTML):
<b>TC-N: Название</b>
• <b>Предусловие:</b> ...
• <b>Шаги:</b> 1. ... 2. ...
• <b>Ожидаемый результат:</b> ...
• <b>Тип:</b> positive/negative/boundary

Покрой: позитивные, негативные и граничные сценарии."""

_BUGREPORT_SYSTEM = """Ты — QA-инженер. Оформляешь баг-репорты в HTML для Telegram.

Формат:
<b>Заголовок:</b> [краткое описание]
<b>Severity:</b> Critical / High / Medium / Low
<b>Priority:</b> High / Medium / Low
<b>Шаги воспроизведения:</b>
1. ...
<b>Фактический результат:</b> ...
<b>Ожидаемый результат:</b> ...
<b>Окружение:</b> [OS, браузер/версия приложения]"""

_THEORY_TOPICS = {
    "design": "техники тест-дизайна: EP, BVA, Decision Table, State Transition, Use Case",
    "levels": "уровни тестирования: компонентное, интеграционное, системное, приёмочное",
    "types": "виды тестирования: функциональное, нефункциональное, структурное, регрессионное, exploratory",
    "principles": "7 принципов тестирования по ISTQB CTFL v4.0",
    "automation": "автоматизация тестирования: инструменты, подходы, пирамида тестирования",
    "mobile": "мобильное тестирование по ISTQB Mobile Tester: native/hybrid/web, эмуляторы vs реальные устройства",
}


async def _get_theory(topic: str) -> str:
    topic_desc = _THEORY_TOPICS.get(topic, topic)
    return await ask_ai(
        f"Объясни подробно тему: {topic_desc}. Дай примеры. Ссылайся на ISTQB."
    )


async def _send_tools(send_fn) -> None:
    text = (
        "🧰 <b>Инструменты QA-тестировщика</b>\n\n"
        "<b>🌐 Web — ручное тестирование</b>\n"
        "• <a href='https://developer.chrome.com/docs/devtools/'>Chrome DevTools</a> — инспектор, сеть, консоль\n"
        "• <a href='https://portswigger.net/burp/communitydownload'>Burp Suite Community</a> — анализ HTTP/API\n\n"
        "<b>🤖 Web — автоматизация UI</b>\n"
        "• <a href='https://playwright.dev/'>Playwright</a> — быстрый, мультибраузерный\n"
        "• <a href='https://www.selenium.dev/'>Selenium</a> — классика\n"
        "• <a href='https://www.cypress.io/'>Cypress</a> — удобный для front-end\n\n"
        "<b>📡 API-тестирование</b>\n"
        "• <a href='https://www.postman.com/'>Postman</a> — GUI для REST/GraphQL\n"
        "• <a href='https://k6.io/'>k6</a> — нагрузочное тестирование\n\n"
        "<b>📱 Mobile</b>\n"
        "• <a href='https://appium.io/'>Appium</a> — iOS и Android автоматизация\n"
        "• <a href='https://www.charlesproxy.com/'>Charles Proxy</a> — перехват трафика\n\n"
        "<b>📋 Трекеры</b>\n"
        "• <a href='https://www.testrail.com/'>TestRail</a> — тест-кейсы\n"
        "• <a href='https://allurereport.org/'>Allure</a> — отчёты\n"
        "• <a href='https://www.atlassian.com/software/jira'>Jira</a> — задачи и баги"
    )
    await send_fn(text, parse_mode="HTML", reply_markup=kb_back_to_menu(),
                  disable_web_page_preview=False)


# ═══════════════════════════════════════════════════════════
# REGISTRATION
# ═══════════════════════════════════════════════════════════

def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("testcase", cmd_testcase))
    app.add_handler(CommandHandler("bugreport", cmd_bugreport))
    app.add_handler(CommandHandler("quiz", cmd_quiz))
    app.add_handler(CommandHandler("theory", cmd_theory))
    app.add_handler(CommandHandler("tools", cmd_tools))
    app.add_handler(CommandHandler("interview", cmd_interview))
    app.add_handler(CommandHandler("ask", cmd_ask))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
