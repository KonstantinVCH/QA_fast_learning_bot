"""QA Bot — handlers v2.2. Inline menu, quiz, theory, tools catalog."""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from .quiz import get_quiz_question, check_answer, get_quiz_stats
from .llm_client import ask_ai as ask_llm

logger = logging.getLogger(__name__)

MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("Квиз ISTQB", callback_data="quiz_start"),
     InlineKeyboardButton("Теория", callback_data="theory_menu")],
    [InlineKeyboardButton("Тест-кейс", callback_data="testcase_help"),
     InlineKeyboardButton("Баг-репорт", callback_data="bugreport_help")],
    [InlineKeyboardButton("Инструменты QA", callback_data="tools_menu"),
     InlineKeyboardButton("Собеседование", callback_data="interview_menu")],
    [InlineKeyboardButton("Задать вопрос", callback_data="ask_question")],
])

THEORY_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("7 принципов тестирования", callback_data="theory_principles")],
    [InlineKeyboardButton("Уровни тестирования", callback_data="theory_levels")],
    [InlineKeyboardButton("Методы черного ящика", callback_data="theory_black_box")],
    [InlineKeyboardButton("Методы белого ящика", callback_data="theory_white_box")],
    [InlineKeyboardButton("Типы тестирования", callback_data="theory_types")],
    [InlineKeyboardButton("Управление тестированием", callback_data="theory_management")],
    [InlineKeyboardButton("Мобильное тестирование (MAT)", callback_data="theory_mobile")],
    [InlineKeyboardButton("Назад", callback_data="main_menu")],
])

TOOLS_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("Jira — трекер задач", url="https://www.atlassian.com/software/jira")],
    [InlineKeyboardButton("TestRail — управление тестами", url="https://www.testrail.com")],
    [InlineKeyboardButton("Postman — тест API", url="https://www.postman.com")],
    [InlineKeyboardButton("Charles Proxy — перехват трафика", url="https://www.charlesproxy.com")],
    [InlineKeyboardButton("Selenium — автоматизация UI", url="https://www.selenium.dev")],
    [InlineKeyboardButton("Appium — мобильная автоматизация", url="https://appium.io")],
    [InlineKeyboardButton("Назад", callback_data="main_menu")],
])

INTERVIEW_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("Вопросы на Junior QA", callback_data="interview_junior")],
    [InlineKeyboardButton("Вопросы по ISTQB", callback_data="interview_istqb")],
    [InlineKeyboardButton("Вопросы по API тестированию", callback_data="interview_api")],
    [InlineKeyboardButton("Вопросы по мобильному тестированию", callback_data="interview_mobile")],
    [InlineKeyboardButton("Назад", callback_data="main_menu")],
])

BACK_MAIN = InlineKeyboardMarkup([
    [InlineKeyboardButton("Главное меню", callback_data="main_menu")]
])

QUIZ_DIFFICULTY = InlineKeyboardMarkup([
    [InlineKeyboardButton("Легкий", callback_data="quiz_easy"),
     InlineKeyboardButton("Средний", callback_data="quiz_medium"),
     InlineKeyboardButton("Сложный", callback_data="quiz_hard")],
    [InlineKeyboardButton("Назад", callback_data="main_menu")],
])

THEORY_CONTENT = {
    "theory_principles": (
        "*7 принципов тестирования (ISTQB CTFL v4.0)*\n\n"
        "1. Тестирование показывает наличие дефектов, а не их отсутствие.\n"
        "Тестирование может показать, что дефекты присутствуют, но не доказать их отсутствие.\n\n"
        "2. Исчерпывающее тестирование невозможно.\n"
        "Проверить все входные данные нереально. Используем анализ рисков и приоритизацию.\n\n"
        "3. Раннее тестирование экономит время и деньги.\n"
        "Чем раньше найден дефект, тем дешевле его исправление.\n\n"
        "4. Скопление дефектов.\n"
        "Большинство дефектов сосредоточено в небольшом числе модулей (правило 80/20).\n\n"
        "5. Парадокс пестицида.\n"
        "Повторяющиеся тесты теряют эффективность. Тесты нужно обновлять.\n\n"
        "6. Тестирование зависит от контекста.\n"
        "Разные системы требуют разных подходов.\n\n"
        "7. Заблуждение об отсутствии ошибок.\n"
        "Отсутствие дефектов не означает, что система отвечает ожиданиям пользователей."
    ),
    "theory_levels": (
        "*Уровни тестирования (ISTQB CTFL v4.0)*\n\n"
        "Компонентное (Unit) тестирование\n"
        "Тестирование отдельных модулей в изоляции. Выполняется разработчиками.\n\n"
        "Интеграционное тестирование\n"
        "Проверка взаимодействия между компонентами. Подходы: восходящее, нисходящее.\n\n"
        "Системное тестирование\n"
        "Тестирование всей системы как единого целого.\n\n"
        "Приемочное тестирование\n"
        "Проверка готовности системы к эксплуатации. UAT, альфа/бета-тестирование."
    ),
    "theory_black_box": (
        "*Методы черного ящика (ISTQB CTFL v4.0)*\n\n"
        "Эквивалентное разбиение\n"
        "Разделение входных данных на классы с одинаковым поведением.\n\n"
        "Анализ граничных значений\n"
        "Тестирование на границах эквивалентных классов. Для 1-100: 0,1,2 и 99,100,101.\n\n"
        "Таблица решений\n"
        "Систематическое тестирование комбинаций условий.\n\n"
        "Тестирование переходов состояний\n"
        "Проверка переходов системы между состояниями.\n\n"
        "Тестирование сценариев использования\n"
        "Тест-кейсы на основе реальных сценариев работы пользователя."
    ),
    "theory_white_box": (
        "*Методы белого ящика (ISTQB CTFL v4.0)*\n\n"
        "Покрытие операторов\n"
        "Каждый оператор кода выполнен хотя бы один раз.\n\n"
        "Покрытие ветвей\n"
        "Каждый логический переход (да/нет) проверен хотя бы раз.\n\n"
        "Покрытие условий\n"
        "Каждое условие принимает значения true и false.\n\n"
        "Тестирование путей\n"
        "Проверка всех возможных путей выполнения в коде."
    ),
    "theory_types": (
        "*Типы тестирования (ISTQB CTFL v4.0)*\n\n"
        "Функциональное тестирование\n"
        "Проверка того, что система делает (функции, бизнес-логика).\n\n"
        "Нефункциональное тестирование\n"
        "Производительность, безопасность, удобство использования, надежность.\n\n"
        "Структурное тестирование\n"
        "Тестирование на основе внутренней структуры кода (белый ящик).\n\n"
        "Тестирование связанное с изменениями\n"
        "Подтверждающее — проверка исправления дефекта.\n"
        "Регрессионное — проверка, что изменения не сломали другое."
    ),
    "theory_management": (
        "*Управление тестированием (ISTQB CTFL v4.0)*\n\n"
        "Тест-план\n"
        "Документ, описывающий стратегию, ресурсы, расписание и область тестирования.\n\n"
        "Оценка тестирования\n"
        "Методы: экспертная оценка, метод точек тестирования, метрики.\n\n"
        "Управление рисками\n"
        "Идентификация, анализ и митигация рисков продукта и проекта.\n\n"
        "Метрики тестирования\n"
        "Плотность дефектов, покрытие требований, DDE."
    ),
    "theory_mobile": (
        "*Мобильное тестирование (ISTQB MAT)*\n\n"
        "Типы мобильных приложений\n"
        "Native — платформо-зависимые (Swift, Kotlin).\n"
        "Hybrid — оболочка вокруг web-view.\n"
        "Web-based — мобильный браузер.\n\n"
        "Эмулятор vs Симулятор\n"
        "Эмулятор — воспроизводит аппаратное и программное обеспечение.\n"
        "Симулятор — только программную среду (iOS Simulator).\n\n"
        "Типы тестирования\n"
        "Инсталляционное, UX, производительность, безопасность, прерывания, совместимость."
    ),
}

INTERVIEW_CONTENT = {
    "interview_junior": (
        "*Топ вопросов на Junior QA*\n\n"
        "1. Что такое тестирование ПО и зачем оно нужно?\n"
        "2. Чем тест-кейс отличается от тест-плана?\n"
        "3. Что такое дефект/баг/ошибка?\n"
        "4. Что такое smoke-тестирование?\n"
        "5. Что такое регрессионное тестирование?\n"
        "6. Что такое приоритет и серьезность дефекта?\n"
        "7. Какой жизненный цикл у дефекта?\n"
        "8. Что такое тестовая среда?\n"
        "9. Разница между black box и white box тестированием?\n"
        "10. Что такое требования и как с ними работать?"
    ),
    "interview_istqb": (
        "*Вопросы по ISTQB на собеседовании*\n\n"
        "1. Назови 7 принципов тестирования.\n"
        "2. Что такое парадокс пестицида?\n"
        "3. Чем подтверждающее тестирование отличается от регрессионного?\n"
        "4. Что такое тестовый оракул?\n"
        "5. Какие уровни тестирования ты знаешь?\n"
        "6. Что такое эквивалентное разбиение и граничные значения?\n"
        "7. В чем разница между верификацией и валидацией?\n"
        "8. Что такое покрытие ветвей?\n"
        "9. Когда применяется таблица решений?\n"
        "10. Что такое тестирование переходов состояний?"
    ),
    "interview_api": (
        "*Вопросы по API тестированию*\n\n"
        "1. Что такое REST API?\n"
        "2. Какие HTTP-методы ты знаешь? (GET, POST, PUT, DELETE, PATCH)\n"
        "3. Что такое статус-коды HTTP? Назови основные.\n"
        "4. Как проверить API без интерфейса?\n"
        "5. Что такое Postman и как его использовать?\n"
        "6. Что такое JSON?\n"
        "7. Что тестируют в API? (статус-код, тело ответа, заголовки, время)\n"
        "8. Что такое авторизация и аутентификация в API?\n"
        "9. Чем REST отличается от SOAP?\n"
        "10. Как тестировать негативные сценарии в API?"
    ),
    "interview_mobile": (
        "*Вопросы по мобильному тестированию*\n\n"
        "1. В чем разница между native, hybrid и web-based приложениями?\n"
        "2. Чем эмулятор отличается от симулятора?\n"
        "3. Что такое тестирование прерываний?\n"
        "4. Как тестировать приложение без интернета?\n"
        "5. Что такое фрагментация в Android?\n"
        "6. Как тестировать потребление батареи?\n"
        "7. Какие инструменты используются для мобильного тестирования?\n"
        "8. Что такое Device Farm?\n"
        "9. Как тестировать push-уведомления?\n"
        "10. Особенности тестирования жестов и Touch ID?"
    ),
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Привет! Я QA Fast Learning Bot\n\n"
        "Помогаю разобраться в тонкостях тестирования.\n"
        "Обновлен по программе ISTQB CTFL v4.0 с вопросами из реального экзамена.\n\n"
        "Выбери раздел:"
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Доступные команды:\n\n"
        "/start — главное меню\n"
        "/quiz — квиз по ISTQB\n"
        "/theory — теория тестирования\n"
        "/testcase — помощь с тест-кейсами\n"
        "/bugreport — помощь с баг-репортами\n"
        "/ask — задать вопрос по QA\n"
        "/interview — подготовка к собеседованию\n"
        "/tools — каталог QA-инструментов\n"
        "/stats — статистика квиза\n"
        "/help — эта справка"
    )
    await update.message.reply_text(text, reply_markup=BACK_MAIN)


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Квиз по ISTQB\n\nВыбери уровень сложности:",
        reply_markup=QUIZ_DIFFICULTY,
    )


async def send_quiz_question(update_or_query, context: ContextTypes.DEFAULT_TYPE, difficulty: str) -> None:
    question = get_quiz_question(difficulty)
    if not question:
        text = "Вопросы для этого уровня закончились! Попробуй другой уровень."
        if hasattr(update_or_query, "message"):
            await update_or_query.message.reply_text(text, reply_markup=QUIZ_DIFFICULTY)
        else:
            await update_or_query.edit_message_text(text, reply_markup=QUIZ_DIFFICULTY)
        return

    context.user_data["current_question"] = question
    context.user_data["quiz_difficulty"] = difficulty

    options = question["options"]
    keyboard = [
        [InlineKeyboardButton(f"A) {options[0]}", callback_data="quiz_answer_0")],
        [InlineKeyboardButton(f"B) {options[1]}", callback_data="quiz_answer_1")],
        [InlineKeyboardButton(f"C) {options[2]}", callback_data="quiz_answer_2")],
        [InlineKeyboardButton(f"D) {options[3]}", callback_data="quiz_answer_3")],
        [InlineKeyboardButton("Пропустить", callback_data=f"quiz_{difficulty}"),
         InlineKeyboardButton("Закончить", callback_data="main_menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    level_label = {"easy": "Легкий", "medium": "Средний", "hard": "Сложный"}[difficulty]
    text = f"{level_label} | Вопрос:\n\n{question['question']}"

    if hasattr(update_or_query, "message"):
        await update_or_query.message.reply_text(text, reply_markup=markup)
    else:
        await update_or_query.edit_message_text(text, reply_markup=markup)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stats = get_quiz_stats(context.user_data)
    text = (
        f"Твоя статистика:\n\n"
        f"Правильных: {stats['correct']}\n"
        f"Неправильных: {stats['wrong']}\n"
        f"Всего вопросов: {stats['total']}\n"
        f"Точность: {stats['accuracy']}%"
    )
    await update.message.reply_text(text, reply_markup=BACK_MAIN)


async def theory_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Теория тестирования\n\nВыбери тему:",
        reply_markup=THEORY_MENU,
    )


async def testcase_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["awaiting"] = "testcase"
    await update.message.reply_text(
        "Генератор тест-кейсов\n\n"
        "Опиши функциональность или требование — я составлю тест-кейсы по ISTQB-стандарту:",
        reply_markup=BACK_MAIN,
    )


async def bugreport_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["awaiting"] = "bugreport"
    await update.message.reply_text(
        "Помощник баг-репорта\n\n"
        "Опиши проблему — я помогу составить грамотный баг-репорт:",
        reply_markup=BACK_MAIN,
    )


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["awaiting"] = "ask"
    await update.message.reply_text(
        "Задай вопрос по QA\n\nСпрашивай всё что интересует по тестированию:",
        reply_markup=BACK_MAIN,
    )


async def interview_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Подготовка к собеседованию\n\nВыбери тему:",
        reply_markup=INTERVIEW_MENU,
    )


async def tools_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Каталог QA-инструментов\n\nПопулярные инструменты с официальными сайтами:",
        reply_markup=TOOLS_MENU,
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    awaiting = context.user_data.get("awaiting")
    text = update.message.text

    if awaiting == "testcase":
        context.user_data.pop("awaiting", None)
        await update.message.reply_text("Генерирую тест-кейсы...")
        prompt = (
            f"Ты опытный QA-инженер, знающий ISTQB CTFL v4.0.\n"
            f"Составь подробные тест-кейсы для следующей функциональности:\n\n{text}\n\n"
            f"Формат каждого тест-кейса:\n"
            f"ID: TC-001\nНазвание: ...\nПредусловия: ...\nШаги: 1. ... 2. ...\n"
            f"Ожидаемый результат: ...\nПриоритет: High/Medium/Low\n\n"
            f"Составь минимум 5 тест-кейсов, включая позитивные и негативные сценарии."
        )
        response = await ask_llm(prompt)
        await update.message.reply_text(response, reply_markup=BACK_MAIN)

    elif awaiting == "bugreport":
        context.user_data.pop("awaiting", None)
        await update.message.reply_text("Составляю баг-репорт...")
        prompt = (
            f"Ты опытный QA-инженер. Составь баг-репорт:\n\n{text}\n\n"
            f"Формат:\nНазвание: ...\nСерьезность: Critical/High/Medium/Low\n"
            f"Приоритет: High/Medium/Low\nОкружение: ...\n"
            f"Шаги воспроизведения:\n1. ...\n2. ...\n"
            f"Фактический результат: ...\nОжидаемый результат: ..."
        )
        response = await ask_llm(prompt)
        await update.message.reply_text(response, reply_markup=BACK_MAIN)

    elif awaiting == "ask":
        context.user_data.pop("awaiting", None)
        await update.message.reply_text("Думаю...")
        prompt = (
            f"Ты эксперт по тестированию ПО с глубоким знанием ISTQB CTFL v4.0.\n"
            f"Ответь на вопрос по QA:\n\n{text}\n\n"
            f"Дай четкий, структурированный ответ. Используй примеры где уместно."
        )
        response = await ask_llm(prompt)
        await update.message.reply_text(response, reply_markup=BACK_MAIN)

    else:
        await update.message.reply_text("Выбери раздел из меню:", reply_markup=MAIN_MENU)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_text("Привет! Выбери раздел:", reply_markup=MAIN_MENU)

    elif data == "theory_menu":
        await query.edit_message_text("Теория тестирования\n\nВыбери тему:", reply_markup=THEORY_MENU)

    elif data in THEORY_CONTENT:
        await query.edit_message_text(THEORY_CONTENT[data], parse_mode="Markdown", reply_markup=BACK_MAIN)

    elif data == "tools_menu":
        await query.edit_message_text("Каталог QA-инструментов:", reply_markup=TOOLS_MENU)

    elif data == "interview_menu":
        await query.edit_message_text("Подготовка к собеседованию:\n\nВыбери тему:", reply_markup=INTERVIEW_MENU)

    elif data in INTERVIEW_CONTENT:
        await query.edit_message_text(INTERVIEW_CONTENT[data], parse_mode="Markdown", reply_markup=BACK_MAIN)

    elif data == "quiz_start":
        await query.edit_message_text("Квиз по ISTQB\n\nВыбери уровень:", reply_markup=QUIZ_DIFFICULTY)

    elif data in ("quiz_easy", "quiz_medium", "quiz_hard"):
        difficulty = data.replace("quiz_", "")
        await send_quiz_question(query, context, difficulty)

    elif data.startswith("quiz_answer_"):
        answer_idx = int(data.split("_")[-1])
        question = context.user_data.get("current_question")
        difficulty = context.user_data.get("quiz_difficulty", "easy")

        if not question:
            await query.edit_message_text("Вопрос не найден. Начнём заново?", reply_markup=QUIZ_DIFFICULTY)
            return

        is_correct, explanation = check_answer(question, answer_idx, context.user_data)
        correct_letter = ["A", "B", "C", "D"][question["correct"]]

        if is_correct:
            result_text = f"Правильно!\n\n{explanation}"
        else:
            chosen_letter = ["A", "B", "C", "D"][answer_idx]
            result_text = (
                f"Неправильно. Ты выбрал: {chosen_letter}\n"
                f"Правильный ответ: {correct_letter}\n\n{explanation}"
            )

        next_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Следующий вопрос", callback_data=f"quiz_{difficulty}")],
            [InlineKeyboardButton("Закончить", callback_data="main_menu")],
        ])
        await query.edit_message_text(result_text, reply_markup=next_keyboard)

    elif data == "testcase_help":
        context.user_data["awaiting"] = "testcase"
        await query.edit_message_text("Генератор тест-кейсов\n\nОпиши функциональность:", reply_markup=BACK_MAIN)

    elif data == "bugreport_help":
        context.user_data["awaiting"] = "bugreport"
        await query.edit_message_text("Помощник баг-репорта\n\nОпиши проблему:", reply_markup=BACK_MAIN)

    elif data == "ask_question":
        context.user_data["awaiting"] = "ask"
        await query.edit_message_text("Задай вопрос по QA:\n\nСпрашивай всё по тестированию:", reply_markup=BACK_MAIN)


def register_handlers(app) -> None:
    """Регистрация обработчиков."""
    from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("theory", theory_command))
    app.add_handler(CommandHandler("testcase", testcase_command))
    app.add_handler(CommandHandler("bugreport", bugreport_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("interview", interview_command))
    app.add_handler(CommandHandler("tools", tools_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
