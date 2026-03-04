"""QA Bot — Telegram handlers v3.0.
Интерактивные инструменты с категориями + подробными статьями.
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes,
)
from .llm_client import ask_ai
from .quiz import QuizSession, QUIZ_BANK
from .tools_data import TOOLS_CATEGORIES, TOOLS_DATA

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════
# KEYBOARDS
# ═══════════════════════════════════════════════════════════

def kb_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧪 Тест-кейсы", callback_data="menu_testcase"),
         InlineKeyboardButton("🐛 Баг-репорт", callback_data="menu_bugreport")],
        [InlineKeyboardButton("❓ Квиз ISTQB", callback_data="menu_quiz"),
         InlineKeyboardButton("📚 Теория", callback_data="menu_theory")],
        [InlineKeyboardButton("🧰 Инструменты QA", callback_data="menu_tools")],
        [InlineKeyboardButton("💼 Собеседование", callback_data="menu_interview"),
         InlineKeyboardButton("💬 Спросить AI", callback_data="menu_ask")],
    ])


def kb_quiz_levels() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Лёгкий", callback_data="quiz_easy"),
         InlineKeyboardButton("🟡 Средний", callback_data="quiz_medium")],
        [InlineKeyboardButton("🔴 Сложный", callback_data="quiz_hard"),
         InlineKeyboardButton("🎲 Микс", callback_data="quiz_mixed")],
        [InlineKeyboardButton("⬅️ Меню", callback_data="menu_main")],
    ])


def kb_quiz_answers() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("A", callback_data="quiz_ans_A"),
         InlineKeyboardButton("B", callback_data="quiz_ans_B"),
         InlineKeyboardButton("C", callback_data="quiz_ans_C"),
         InlineKeyboardButton("D", callback_data="quiz_ans_D")],
        [InlineKeyboardButton("❌ Прервать квиз", callback_data="quiz_stop")],
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


def kb_tools_categories() -> InlineKeyboardMarkup:
    """Кнопки категорий инструментов."""
    rows = []
    items = list(TOOLS_CATEGORIES.items())
    for i in range(0, len(items), 2):
        row = []
        for cat_id, cat_data in items[i:i+2]:
            row.append(InlineKeyboardButton(
                cat_data["name"],
                callback_data=f"tools_cat_{cat_id}"
            ))
        rows.append(row)
    rows.append([InlineKeyboardButton("⬅️ Главное меню", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def kb_tools_in_category(category_id: str) -> InlineKeyboardMarkup:
    """Кнопки инструментов внутри категории."""
    cat = TOOLS_CATEGORIES.get(category_id, {})
    tools = cat.get("tools", [])
    rows = []
    for tool_id in tools:
        tool = TOOLS_DATA.get(tool_id, {})
        name = f"{tool.get('emoji', '')} {tool.get('name', tool_id)}"
        rows.append([InlineKeyboardButton(name, callback_data=f"tool_view_{tool_id}")])
    rows.append([InlineKeyboardButton("⬅️ Категории", callback_data="menu_tools")])
    return InlineKeyboardMarkup(rows)


def kb_tool_sections(tool_id: str) -> InlineKeyboardMarkup:
    """Разделы одного инструмента."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Установка", callback_data=f"tool_sec_{tool_id}_install"),
         InlineKeyboardButton("⚙️ Функции", callback_data=f"tool_sec_{tool_id}_features")],
        [InlineKeyboardButton("💡 Примеры", callback_data=f"tool_sec_{tool_id}_usage"),
         InlineKeyboardButton("🔗 Документация", callback_data=f"tool_sec_{tool_id}_docs")],
        [InlineKeyboardButton("⬅️ Назад", callback_data=f"tools_cat_{TOOLS_DATA.get(tool_id, {}).get('category', '')}")],
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
    "Обучаю по программе <b>ISTQB CTFL v4.0</b> и помогаю с реальными задачами.\n\n"
    "Выбери раздел:"
)

# ═══════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    await _send_tools_menu(update.message.reply_text)


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
# TOOLS HELPERS
# ═══════════════════════════════════════════════════════════

async def _send_tools_menu(send_fn, **kwargs):
    """Отправить главное меню инструментов."""
    total_tools = len(TOOLS_DATA)
    text = (
        f"🧰 <b>Инструменты QA-инженера</b>\n\n"
        f"📚 База знаний: <b>{total_tools} инструментов</b>\n"
        "Для каждого: установка, настройка, примеры использования.\n\n"
        "Выбери категорию:"
    )
    await send_fn(text, parse_mode="HTML", reply_markup=kb_tools_categories(), **kwargs)


def _build_tool_overview(tool_id: str) -> str:
    """Краткая карточка инструмента."""
    t = TOOLS_DATA.get(tool_id)
    if not t:
        return "❌ Инструмент не найден"
    tips_text = "\n".join(t.get("tips", []))
    return (
        f"{t['emoji']} <b>{t['name']}</b>\n"
        f"<i>{t['tagline']}</i>\n\n"
        f"{t['description']}\n\n"
        f"{tips_text}\n\n"
        f"Выбери раздел для подробностей:"
    )


def _build_tool_section(tool_id: str, section: str) -> str:
    """Конкретный раздел инструмента."""
    t = TOOLS_DATA.get(tool_id)
    if not t:
        return "❌ Инструмент не найден"

    if section == "install":
        return f"{t['emoji']} <b>{t['name']} — Установка</b>\n\n{t['install']}"
    elif section == "features":
        return f"{t['emoji']} <b>{t['name']} — Функции</b>\n\n{t['features']}"
    elif section == "usage":
        return f"{t['emoji']} <b>{t['name']} — Примеры</b>\n\n{t['usage_example']}"
    elif section == "docs":
        tips = "\n".join(t.get("tips", []))
        return (
            f"{t['emoji']} <b>{t['name']} — Документация</b>\n\n"
            f"🔗 <a href='{t['docs_url']}'>Официальная документация</a>\n\n"
            f"<b>Советы:</b>\n{tips}"
        )
    return "❌ Раздел не найден"


# ═══════════════════════════════════════════════════════════
# CALLBACK HANDLER
# ═══════════════════════════════════════════════════════════

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    async def edit(text, markup=None, preview=False):
        try:
            await query.message.edit_text(
                text, parse_mode="HTML", reply_markup=markup,
                disable_web_page_preview=not preview
            )
        except Exception:
            await query.message.reply_text(
                text, parse_mode="HTML", reply_markup=markup,
                disable_web_page_preview=not preview
            )

    # ── Main menu ─────────────────────────────────────────
    if data == "menu_main":
        context.user_data.clear()
        await edit(WELCOME_TEXT, kb_main_menu())

    elif data == "menu_testcase":
        context.user_data["mode"] = "testcase"
        await edit("🧪 <b>Генерация тест-кейсов</b>\n\nОпиши функциональность:", kb_back_to_menu())

    elif data == "menu_bugreport":
        context.user_data["mode"] = "bugreport"
        await edit("🐛 <b>Оформление баг-репорта</b>\n\nОпиши проблему:", kb_back_to_menu())

    elif data == "menu_quiz":
        await edit(
            f"❓ <b>Квиз по ISTQB</b>\n\nБаза: {len(QUIZ_BANK)} вопросов. Выбери уровень:",
            kb_quiz_levels()
        )

    elif data == "menu_theory":
        await edit("📚 <b>Теория тестирования</b>\n\nВыбери тему:", kb_theory_topics())

    elif data == "menu_tools":
        total_tools = len(TOOLS_DATA)
        await edit(
            f"🧰 <b>Инструменты QA-инженера</b>\n\n"
            f"📚 База знаний: <b>{total_tools} инструментов</b>\n"
            "Для каждого: установка, настройка, примеры.\n\n"
            "Выбери категорию:",
            kb_tools_categories()
        )

    elif data == "menu_interview":
        context.user_data["mode"] = "interview"
        await edit("💼 <b>Собеседование</b>\n\nНапиши тему — дам вопросы и ответы:", kb_back_to_menu())

    elif data == "menu_ask":
        context.user_data["mode"] = "ask"
        await edit("💬 <b>AI-эксперт</b>\n\nЗадай любой вопрос по QA:", kb_back_to_menu())

    # ── Tools: category ───────────────────────────────────
    elif data.startswith("tools_cat_"):
        cat_id = data[10:]
        cat = TOOLS_CATEGORIES.get(cat_id, {})
        if not cat:
            await edit("❌ Категория не найдена", kb_tools_categories())
            return
        tools_list = cat.get("tools", [])
        tools_preview = ""
        for tid in tools_list:
            t = TOOLS_DATA.get(tid, {})
            tools_preview += f"• {t.get('emoji','')} <b>{t.get('name', tid)}</b> — {t.get('tagline','')}\n"
        text = (
            f"{cat['name']}\n"
            f"<i>{cat['description']}</i>\n\n"
            f"{tools_preview}\n"
            "Выбери инструмент:"
        )
        await edit(text, kb_tools_in_category(cat_id))

    # ── Tools: view tool overview ─────────────────────────
    elif data.startswith("tool_view_"):
        tool_id = data[10:]
        text = _build_tool_overview(tool_id)
        await edit(text, kb_tool_sections(tool_id))

    # ── Tools: view section ───────────────────────────────
    elif data.startswith("tool_sec_"):
        # tool_sec_{tool_id}_{section}
        parts = data[9:].rsplit("_", 1)
        if len(parts) == 2:
            tool_id, section = parts
            text = _build_tool_section(tool_id, section)
            await edit(text, kb_tool_sections(tool_id))

    # ── Quiz level selection ──────────────────────────────
    elif data.startswith("quiz_") and not data.startswith("quiz_ans_") and data != "quiz_stop":
        level = data[5:]
        session = QuizSession(level=level)
        context.user_data["quiz"] = session
        context.user_data["mode"] = "quiz"
        await edit(session.current_question(), kb_quiz_answers())

    # ── Quiz answers ──────────────────────────────────────
    elif data.startswith("quiz_ans_"):
        answer_letter = data[9:]
        session: QuizSession | None = context.user_data.get("quiz")
        if not session or session.is_finished:
            await edit("Квиз завершён. Начни новый через /quiz или меню.", kb_main_menu())
            return
        response = session.answer(answer_letter)
        if session.is_finished:
            context.user_data.pop("mode", None)
            context.user_data.pop("quiz", None)
            await edit(response, kb_main_menu())
        else:
            await edit(response, kb_quiz_answers())

    elif data == "quiz_stop":
        context.user_data.pop("mode", None)
        context.user_data.pop("quiz", None)
        await edit("Квиз прерван. Возвращайся когда будешь готов! 💪", kb_main_menu())

    # ── Theory ────────────────────────────────────────────
    elif data.startswith("theory_"):
        topic = data[7:]
        await query.message.edit_text("⏳ Загружаю теорию...", parse_mode="HTML")
        content = await _get_theory(topic)
        await edit(content, kb_theory_topics())


# ═══════════════════════════════════════════════════════════
# MESSAGE HANDLER
# ═══════════════════════════════════════════════════════════

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    mode = context.user_data.get("mode", "ask")

    if mode == "quiz":
        session: QuizSession | None = context.user_data.get("quiz")
        if session and not session.is_finished:
            await update.message.reply_text(
                "👆 Используй кнопки A / B / C / D для ответа",
                reply_markup=kb_quiz_answers()
            )
            return

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
# THEORY CONTENT
# ═══════════════════════════════════════════════════════════

async def _get_theory(topic: str) -> str:
    """Возвращает теорию по теме — из базы или через AI."""
    if topic in _THEORY_STATIC:
        return _THEORY_STATIC[topic]
    # AI fallback
    response = await ask_ai(
        f"Объясни подробно тему тестирования: «{topic}»\n"
        "Используй ISTQB терминологию. Приведи примеры. HTML форматирование."
    )
    return response


_THEORY_STATIC = {
    "design": (
        "📐 <b>Техники тест-дизайна (ISTQB CTFL 4.2)</b>\n\n"
        "<b>1. Эквивалентное разбиение (EP)</b>\n"
        "Делим входные данные на классы, где все значения обрабатываются одинаково.\n"
        "<i>Пример:</i> Поле «Возраст» 18-65:\n"
        "• Класс 1: &lt;18 (невалидный)\n"
        "• Класс 2: 18-65 (валидный)\n"
        "• Класс 3: &gt;65 (невалидный)\n"
        "Тестируем: 15, 30, 70\n\n"
        "<b>2. Анализ граничных значений (BVA)</b>\n"
        "Тестируем значения на границах диапазона.\n"
        "<i>Пример:</i> Для диапазона 18-65:\n"
        "Тестируем: 17, 18, 19, 64, 65, 66\n\n"
        "<b>3. Таблица решений</b>\n"
        "Все комбинации условий → действия системы.\n"
        "<i>Применяем:</i> когда логика зависит от нескольких условий.\n\n"
        "<b>4. Переходы состояний</b>\n"
        "Система как машина состояний: тестируем переходы.\n"
        "<i>Пример:</i> Заказ: Created → Paid → Shipped → Delivered\n\n"
        "<b>5. Попарное тестирование (Pairwise)</b>\n"
        "Покрываем все пары параметров вместо всех комбинаций.\n"
        "Инструмент: <a href='https://www.pairwise.org/'>pairwise.org</a>"
    ),
    "levels": (
        "🔬 <b>Уровни тестирования (ISTQB CTFL 2.2)</b>\n\n"
        "<b>1. Компонентное / Unit тестирование</b>\n"
        "• Тестируем отдельные функции/классы в изоляции\n"
        "• Кто: разработчики\n"
        "• Инструменты: pytest, JUnit, NUnit\n"
        "• Быстрые, много, дешёвые\n\n"
        "<b>2. Интеграционное тестирование</b>\n"
        "• Взаимодействие между компонентами (модули, API, БД)\n"
        "• Подходы: Big Bang, Top-Down, Bottom-Up, Sandwich\n"
        "• Инструменты: Postman, REST Assured\n\n"
        "<b>3. Системное тестирование</b>\n"
        "• Вся система как единое целое\n"
        "• Функциональное + нефункциональное (производительность, безопасность)\n"
        "• Кто: QA команда\n\n"
        "<b>4. Приёмочное тестирование (UAT)</b>\n"
        "• Соответствует ли система требованиям бизнеса?\n"
        "• Кто: заказчик / пользователи\n"
        "• Подходы: Alpha testing, Beta testing\n\n"
        "🏛️ <b>Пирамида тестирования:</b>\n"
        "много Unit → меньше Integration → мало E2E\n"
        "Чем выше — тем медленнее и дороже"
    ),
    "types": (
        "⚡ <b>Виды тестирования</b>\n\n"
        "<b>По знанию системы:</b>\n"
        "• <b>Black Box</b> — тестируем поведение, не видя код\n"
        "• <b>White Box</b> — тестируем с доступом к коду\n"
        "• <b>Grey Box</b> — частичное знание внутренней структуры\n\n"
        "<b>По цели:</b>\n"
        "• <b>Smoke</b> — быстрая проверка ключевых функций сборки\n"
        "• <b>Sanity</b> — проверка конкретного исправления/функции\n"
        "• <b>Regression</b> — проверка что ничего не сломали\n"
        "• <b>Exploratory</b> — исследование без скрипта\n"
        "• <b>Load</b> — поведение при ожидаемой нагрузке\n"
        "• <b>Stress</b> — поведение за пределами нормы\n"
        "• <b>Security</b> — уязвимости и защита данных\n"
        "• <b>Usability</b> — удобство использования\n"
        "• <b>Compatibility</b> — браузеры, устройства, ОС\n\n"
        "<b>По автоматизации:</b>\n"
        "• <b>Manual</b> — ручное выполнение\n"
        "• <b>Automated</b> — Selenium, Playwright, Cypress"
    ),
    "principles": (
        "📋 <b>7 принципов тестирования ISTQB (CTFL 1.3)</b>\n\n"
        "<b>1. Тестирование показывает наличие дефектов</b>\n"
        "Нельзя доказать отсутствие багов — только наличие.\n\n"
        "<b>2. Исчерпывающее тестирование невозможно</b>\n"
        "Проверить все входные данные нереально → расставляй приоритеты.\n\n"
        "<b>3. Раннее тестирование</b>\n"
        "Чем раньше найден баг — тем дешевле исправить.\n"
        "Баг в требованиях: $1 → в разработке: $10 → в production: $100+\n\n"
        "<b>4. Скопление дефектов (Pesticide Paradox)</b>\n"
        "Баги кластеризуются в модулях. 80% багов — в 20% кода.\n\n"
        "<b>5. Тестирование зависит от контекста</b>\n"
        "Для банка и игры — разные подходы.\n\n"
        "<b>6. Заблуждение об отсутствии ошибок</b>\n"
        "Нет багов ≠ хороший продукт. Может не соответствовать ожиданиям.\n\n"
        "<b>7. Парадокс пестицида</b>\n"
        "Одни и те же тесты перестают находить новые баги → обновляй тесты."
    ),
    "automation": (
        "🤖 <b>Автоматизация тестирования</b>\n\n"
        "<b>Когда автоматизировать:</b>\n"
        "✅ Регрессионные тесты (запускаются часто)\n"
        "✅ Smoke тесты (быстрая проверка сборки)\n"
        "✅ Data-driven тесты (много наборов данных)\n"
        "❌ Одноразовые тесты\n"
        "❌ UI тесты с частыми изменениями\n\n"
        "<b>Инструменты:</b>\n"
        "• <b>Web UI:</b> Selenium, Playwright, Cypress\n"
        "• <b>API:</b> Postman/Newman, REST Assured, pytest+requests\n"
        "• <b>Mobile:</b> Appium\n"
        "• <b>Нагрузка:</b> JMeter, k6\n\n"
        "<b>Паттерн Page Object Model (POM):</b>\n"
        "Отделяем логику взаимодействия с UI от тестовой логики.\n"
        "<pre>class LoginPage:\n  def login(self, email, password):\n    self.driver.find_element(By.ID, 'email').send_keys(email)\n    ...</pre>\n\n"
        "<b>Пирамида автоматизации:</b>\n"
        "70% Unit + 20% API + 10% E2E = оптимальный баланс"
    ),
    "mobile": (
        "📱 <b>Mobile тестирование (ISTQB Mobile Tester)</b>\n\n"
        "<b>Типы мобильных приложений:</b>\n"
        "• <b>Native</b> — Swift/Kotlin, лучший UX, только одна платформа\n"
        "• <b>Hybrid</b> — HTML в нативной оболочке (Cordova, Ionic)\n"
        "• <b>Web-based</b> — мобильный браузер, адаптивный дизайн\n\n"
        "<b>Что тестировать:</b>\n"
        "📱 Реальные устройства — финальное тестирование\n"
        "💻 Эмуляторы/симуляторы — разработка тестов\n"
        "☁️ BrowserStack/Sauce Labs — облачные фермы устройств\n\n"
        "<b>Особенности мобильного тестирования:</b>\n"
        "• Прерывания: звонок, SMS, уведомления\n"
        "• Смена ориентации (portrait/landscape)\n"
        "• Слабый интернет (3G, Edge, офлайн)\n"
        "• Разные разрешения экранов\n"
        "• Жизненный цикл приложения (фон/передний план)\n"
        "• Разрешения (камера, геолокация, уведомления)\n\n"
        "<b>Инструменты:</b>\n"
        "• Appium — автоматизация iOS/Android\n"
        "• Charles Proxy — перехват трафика\n"
        "• Android Studio / Xcode — встроенные эмуляторы"
    ),
}


# ═══════════════════════════════════════════════════════════
# AI SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════

_TESTCASE_SYSTEM = """Ты — QA-инженер. Пишешь тест-кейсы по ISTQB-стандарту в HTML для Telegram.

Формат каждого тест-кейса (HTML):
<b>TC-N: Название</b>
• <b>Предусловие:</b> ...
• <b>Шаги:</b> 1. ... 2. ...
• <b>Ожидаемый результат:</b> ...
• <b>Техника:</b> [EP/BVA/Decision Table/State Transition]

Пиши 5-8 тест-кейсов. Покрывай: позитивные, негативные, граничные значения.
Отвечай строго на русском."""

_BUGREPORT_SYSTEM = """Ты — QA-инженер. Оформляешь баг-репорты по стандарту в HTML для Telegram.

Формат (строго):
<b>🐛 Заголовок:</b> [Модуль] Краткое описание

<b>📊 Серьёзность:</b> Critical/High/Medium/Low
<b>⚡ Приоритет:</b> Blocker/High/Medium/Low
<b>🌍 Окружение:</b> ОС, браузер, версия

<b>📋 Шаги воспроизведения:</b>
1. ...
2. ...

<b>✅ Ожидаемый результат:</b> ...
<b>❌ Фактический результат:</b> ...

<b>📎 Вложения:</b> screenshot/video/log

Если данных мало — заполни что можешь, остальное отметь как [уточнить].
Отвечай строго на русском."""


# ═══════════════════════════════════════════════════════════
# APP FACTORY
# ═══════════════════════════════════════════════════════════

def build_app(token: str) -> Application:
    """Build and configure the Telegram Application."""
    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("testcase", cmd_testcase))
    app.add_handler(CommandHandler("bugreport", cmd_bugreport))
    app.add_handler(CommandHandler("quiz", cmd_quiz))
    app.add_handler(CommandHandler("theory", cmd_theory))
    app.add_handler(CommandHandler("tools", cmd_tools))
    app.add_handler(CommandHandler("interview", cmd_interview))
    app.add_handler(CommandHandler("ask", cmd_ask))

    # Callbacks and messages
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app
