"""QA Bot вЂ” Telegram handlers v2.2. Inline keyboards, inline quiz answers."""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes,
)
from .llm_client import ask_ai
from .quiz import QuizSession, QUIZ_BANK

logger = logging.getLogger(__name__)

# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
# KEYBOARDS
# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ

def kb_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("рџ“‹ Р“РµРЅРµСЂРёСЂРѕРІР°С‚СЊ С‚РµСЃС‚-РєРµР№СЃС‹", callback_data="menu_testcase"),
         InlineKeyboardButton("рџђ› РЎРѕСЃС‚Р°РІРёС‚СЊ Р±Р°Рі-СЂРµРїРѕСЂС‚", callback_data="menu_bugreport")],
        [InlineKeyboardButton("рџЋЇ РљРІРёР· ISTQB", callback_data="menu_quiz"),
         InlineKeyboardButton("рџ“љ РўРµРѕСЂРёСЏ", callback_data="menu_theory")],
        [InlineKeyboardButton("рџ›  РРЅСЃС‚СЂСѓРјРµРЅС‚С‹ QA", callback_data="menu_tools"),
         InlineKeyboardButton("рџ’ј РџРѕРґРіРѕС‚РѕРІРєР° Рє СЃРѕР±РµСЃРµРґРѕРІР°РЅРёСЋ", callback_data="menu_interview")],
        [InlineKeyboardButton("рџ’¬ РЎРїСЂРѕСЃРёС‚СЊ AI", callback_data="menu_ask")],
    ])


def kb_quiz_levels() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("рџџў Р›С‘РіРєРёР№", callback_data="quiz_easy"),
         InlineKeyboardButton("рџџЎ РЎСЂРµРґРЅРёР№", callback_data="quiz_medium")],
        [InlineKeyboardButton("рџ”ґ РЎР»РѕР¶РЅС‹Р№", callback_data="quiz_hard"),
         InlineKeyboardButton("рџЋІ РњРёРєСЃ", callback_data="quiz_mixed")],
        [InlineKeyboardButton("в—ЂпёЏ РќР°Р·Р°Рґ", callback_data="menu_main")],
    ])


def kb_theory_topics() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("рџ“ђ РњРµС‚РѕРґС‹ С‚РµСЃС‚-РґРёР·Р°Р№РЅР°", callback_data="theory_design"),
         InlineKeyboardButton("рџ“Љ РЈСЂРѕРІРЅРё С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ", callback_data="theory_levels")],
        [InlineKeyboardButton("рџ”¬ Р’РёРґС‹ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ", callback_data="theory_types"),
         InlineKeyboardButton("рџ“‹ ISTQB РїСЂРёРЅС†РёРїС‹", callback_data="theory_principles")],
        [InlineKeyboardButton("рџ¤– РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЏ", callback_data="theory_automation"),
         InlineKeyboardButton("рџ“± Mobile С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ", callback_data="theory_mobile")],
        [InlineKeyboardButton("в—ЂпёЏ РќР°Р·Р°Рґ", callback_data="menu_main")],
    ])


def kb_back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("в—ЂпёЏ Р“Р»Р°РІРЅРѕРµ РјРµРЅСЋ", callback_data="menu_main")]
    ])


# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
# WELCOME TEXT
# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ

WELCOME_TEXT = (
    "рџ‘‹ <b>РџСЂРёРІРµС‚! РЇ QA Fast Learning Bot</b> рџљЂ\n\n"
    "РџРѕРјРѕРіР°СЋ СЂР°Р·Р±РёСЂР°С‚СЊСЃСЏ РІ С‚РѕРЅРєРѕСЃС‚СЏС… С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ.\n"
    "рџ”Ґ РћР±РЅРѕРІР»С‘РЅ РїРѕ РїСЂРѕРіСЂР°РјРјРµ <b>ISTQB CTFL v4.0</b> СЃ РІРѕРїСЂРѕСЃР°РјРё РёР· СЂРµР°Р»СЊРЅРѕРіРѕ СЌРєР·Р°РјРµРЅР°.\n\n"
    "Р’С‹Р±РµСЂРё СЂР°Р·РґРµР»:"
)

# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
# COMMAND HANDLERS
# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message. No photo to avoid slow loading."""
    await update.message.reply_text(
        WELCOME_TEXT, parse_mode="HTML", reply_markup=kb_main_menu()
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "рџ“– <b>Р”РѕСЃС‚СѓРїРЅС‹Рµ РєРѕРјР°РЅРґС‹:</b>\n\n"
        "/start вЂ” РіР»Р°РІРЅРѕРµ РјРµРЅСЋ\n"
        "/testcase вЂ” РіРµРЅРµСЂРёСЂРѕРІР°С‚СЊ С‚РµСЃС‚-РєРµР№СЃС‹\n"
        "/bugreport вЂ” СЃРѕСЃС‚Р°РІРёС‚СЊ Р±Р°Рі-СЂРµРїРѕСЂС‚\n"
        "/quiz вЂ” РєРІРёР· РїРѕ ISTQB\n"
        "/theory вЂ” С‚РµРѕСЂРёСЏ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ\n"
        "/tools вЂ” РёРЅСЃС‚СЂСѓРјРµРЅС‚С‹ QA\n"
        "/interview вЂ” РїРѕРґРіРѕС‚РѕРІРєР° Рє СЃРѕР±РµСЃРµРґРѕРІР°РЅРёСЋ\n"
        "/ask вЂ” Р·Р°РґР°С‚СЊ РІРѕРїСЂРѕСЃ AI\n\n"
        "<i>РР»Рё РїСЂРѕСЃС‚Рѕ РЅР°РїРёС€Рё РІРѕРїСЂРѕСЃ вЂ” СЏ РѕС‚РІРµС‡Сѓ!</i>"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_testcase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "testcase"
    text = (
        "рџ“‹ <b>Р“РµРЅРµСЂР°С†РёСЏ С‚РµСЃС‚-РєРµР№СЃРѕРІ</b>\n\n"
        "РћРїРёС€Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅРѕСЃС‚СЊ вЂ” СЏ СЃРѕР·РґР°Рј С‚РµСЃС‚-РєРµР№СЃС‹ РїРѕ ISTQB-СЃС‚Р°РЅРґР°СЂС‚Р°Рј.\n\n"
        "<i>РџСЂРёРјРµСЂ:</i>\n"
        "В«Р¤РѕСЂРјР° РІС…РѕРґР°: РїРѕР»Рµ email Рё РїР°СЂРѕР»СЊ. Email РґРѕР»Р¶РµРЅ СЃРѕРѕС‚РІРµС‚СЃС‚РІРѕРІР°С‚СЊ С„РѕСЂРјР°С‚Сѓ. "
        "РЎРґРµР»Р°Р№ 5 С‚РµСЃС‚-РєРµР№СЃРѕРІ: РїРѕР·РёС‚РёРІРЅС‹Рµ + РЅРµРіР°С‚РёРІРЅС‹Рµ СЃ РіСЂР°РЅРёС‡РЅС‹РјРё Р·РЅР°С‡РµРЅРёСЏРјРё.В»"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_bugreport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "bugreport"
    text = (
        "рџђ› <b>РЎРѕСЃС‚Р°РІР»РµРЅРёРµ Р±Р°Рі-СЂРµРїРѕСЂС‚Р°</b>\n\n"
        "РћРїРёС€Рё Р±Р°Рі вЂ” СЏ СЃРѕСЃС‚Р°РІР»СЋ РµРіРѕ РїРѕ СЃС‚Р°РЅРґР°СЂС‚Р°Рј.\n\n"
        "<i>РџСЂРёРјРµСЂ:</i>\n"
        "В«РџСЂРё РЅР°Р¶Р°С‚РёРё РєРЅРѕРїРєРё РІРѕ РІРєР»Р°РґРєРµ 7 СЃРёСЃС‚РµРјР° РІС‹Р±СЂР°СЃС‹РІР°РµС‚ РёСЃРєР»СЋС‡РµРЅРёРµ NullPointerException 8.В»"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"рџЋЇ <b>РљРІРёР· РїРѕ ISTQB</b>\n\n"
        f"Р’СЃРµРіРѕ: {len(QUIZ_BANK)} РІРѕРїСЂРѕСЃРѕРІ РёР· РѕС„РёС†РёР°Р»СЊРЅРѕР№ РїСЂРѕРіСЂР°РјРјС‹ ISTQB.\n"
        "Р’С‹Р±РµСЂРё СѓСЂРѕРІРµРЅСЊ СЃР»РѕР¶РЅРѕСЃС‚Рё:"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_quiz_levels())


async def cmd_theory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "рџ“љ <b>РўРµРѕСЂРёСЏ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ</b>\n\nР’С‹Р±РµСЂРё С‚РµРјСѓ:",
        parse_mode="HTML",
        reply_markup=kb_theory_topics(),
    )


async def cmd_tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_tools(update.message.reply_text)


async def cmd_interview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "interview"
    text = (
        "рџ’ј <b>РџРѕРґРіРѕС‚РѕРІРєР° Рє СЃРѕР±РµСЃРµРґРѕРІР°РЅРёСЋ</b>\n\n"
        "РЈРєР°Р¶Рё С‚РµРјСѓ вЂ” Рё СЏ РґР°Рј С‚РёРїРёС‡РЅС‹Рµ РІРѕРїСЂРѕСЃС‹ СЃ СЂР°Р·РІС‘СЂРЅСѓС‚С‹РјРё РѕС‚РІРµС‚Р°РјРё.\n\n"
        "РџСЂРёРјРµСЂС‹:\n"
        "в–Є В«Р’РѕРїСЂРѕСЃС‹ РїРѕ С‚РµРѕСЂРёРё С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏВ»\n"
        "в–Є В«API С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ РЅР° СЃРѕР±РµСЃРµРґРѕРІР°РЅРёРёВ»\n"
        "в–Є В«РљР°Рє РѕС‚РІРµС‡Р°С‚СЊ РЅР° РІРѕРїСЂРѕСЃС‹ Рѕ РЅР°Р№РґРµРЅРЅС‹С… Р±Р°РіР°С…В»"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb_back_to_menu())


async def cmd_ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "ask"
    await update.message.reply_text(
        "рџ’¬ <b>РЎРїСЂРѕСЃРёС‚СЊ AI-Р°СЃСЃРёСЃС‚РµРЅС‚Р°</b>\n\nРќР°РїРёС€Рё Р»СЋР±РѕР№ РІРѕРїСЂРѕСЃ РїРѕ QA:",
        parse_mode="HTML",
        reply_markup=kb_back_to_menu(),
    )


# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
# CALLBACK HANDLER
# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # в”Ђв”Ђ Quiz answer (A/B/C/D) в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    if data.startswith("quiz_answer_"):
        letter = data[-1]  # last char: A, B, C, or D
        session: QuizSession | None = context.user_data.get("quiz")
        if not session or session.is_finished:
            await query.message.edit_text(
                "РљРІРёР· Р·Р°РІРµСЂС€С‘РЅ. РќР°С‡РЅРё РЅРѕРІС‹Р№: /quiz",
                reply_markup=kb_main_menu()
            )
            return

        response = session.answer_by_letter(letter)

        if session.is_finished:
            # Quiz done вЂ” show summary + main menu
            context.user_data.pop("mode", None)
            context.user_data.pop("quiz", None)
            await query.message.edit_text(
                response, parse_mode="HTML", reply_markup=kb_main_menu()
            )
        else:
            # Next question вЂ” show with answer keyboard
            await query.message.edit_text(
                response, parse_mode="HTML",
                reply_markup=session.get_answer_keyboard()
            )
        return

    # в”Ђв”Ђ Main menu navigation в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    if data == "menu_main":
        await query.message.edit_text(
            WELCOME_TEXT, parse_mode="HTML", reply_markup=kb_main_menu()
        )
    elif data == "menu_testcase":
        context.user_data["mode"] = "testcase"
        await query.message.edit_text(
            "рџ“‹ <b>Р“РµРЅРµСЂР°С†РёСЏ С‚РµСЃС‚-РєРµР№СЃРѕРІ</b>\n\nРћРїРёС€Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅРѕСЃС‚СЊ:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )
    elif data == "menu_bugreport":
        context.user_data["mode"] = "bugreport"
        await query.message.edit_text(
            "рџђ› <b>РЎРѕСЃС‚Р°РІР»РµРЅРёРµ Р±Р°Рі-СЂРµРїРѕСЂС‚Р°</b>\n\nРћРїРёС€Рё РїСЂРѕР±Р»РµРјСѓ:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )
    elif data == "menu_quiz":
        await query.message.edit_text(
            f"рџЋЇ <b>РљРІРёР· РїРѕ ISTQB</b>\n\nР’СЃРµРіРѕ: {len(QUIZ_BANK)} РІРѕРїСЂРѕСЃРѕРІ. Р’С‹Р±РµСЂРё СѓСЂРѕРІРµРЅСЊ:",
            parse_mode="HTML", reply_markup=kb_quiz_levels()
        )
    elif data == "menu_theory":
        await query.message.edit_text(
            "рџ“љ <b>РўРµРѕСЂРёСЏ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ</b>\n\nР’С‹Р±РµСЂРё С‚РµРјСѓ:",
            parse_mode="HTML", reply_markup=kb_theory_topics()
        )
    elif data == "menu_tools":
        await _send_tools(
            lambda t, **kw: query.message.edit_text(t, **kw)
        )
    elif data == "menu_interview":
        context.user_data["mode"] = "interview"
        await query.message.edit_text(
            "рџ’ј <b>РџРѕРґРіРѕС‚РѕРІРєР° Рє СЃРѕР±РµСЃРµРґРѕРІР°РЅРёСЋ</b>\n\nРќР°РїРёС€Рё С‚РµРјСѓ вЂ” СЏ РґР°Рј РІРѕРїСЂРѕСЃС‹ Рё РѕС‚РІРµС‚С‹:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )
    elif data == "menu_ask":
        context.user_data["mode"] = "ask"
        await query.message.edit_text(
            "рџ’¬ <b>AI-Р°СЃСЃРёСЃС‚РµРЅС‚</b>\n\nРќР°РїРёС€Рё Р»СЋР±РѕР№ РІРѕРїСЂРѕСЃ РїРѕ QA:",
            parse_mode="HTML", reply_markup=kb_back_to_menu()
        )

    # в”Ђв”Ђ Quiz level selection в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    elif data.startswith("quiz_") and not data.startswith("quiz_answer_"):
        level = data[5:]  # easy / medium / hard / mixed
        session = QuizSession(level=level)
        context.user_data["quiz"] = session
        context.user_data["mode"] = "quiz"
        # Show first question WITH answer keyboard
        await query.message.edit_text(
            session.current_question(),
            parse_mode="HTML",
            reply_markup=session.get_answer_keyboard(),
        )

    # в”Ђв”Ђ Theory topics в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    elif data.startswith("theory_"):
        topic = data[7:]
        await query.message.edit_text("вЏі Р—Р°РіСЂСѓР¶Р°СЋ С‚РµРѕСЂРёСЋ...", parse_mode="HTML")
        content = await _get_theory(topic)
        await query.message.edit_text(
            content, parse_mode="HTML", reply_markup=kb_theory_topics(),
            disable_web_page_preview=True
        )


# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
# MESSAGE HANDLER
# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    mode = context.user_data.get("mode", "ask")

    # Quiz mode: users now use inline buttons, not text.
    # But handle text input as fallback in case quiz is active.
    if mode == "quiz":
        session: QuizSession | None = context.user_data.get("quiz")
        if session and not session.is_finished:
            # Hint user to use buttons
            await update.message.reply_text(
                "рџ‘† РСЃРїРѕР»СЊР·СѓР№ РєРЅРѕРїРєРё РІС‹С€Рµ РґР»СЏ РѕС‚РІРµС‚Р° РЅР° РІРѕРїСЂРѕСЃ.",
                reply_markup=session.get_answer_keyboard()
            )
            return

    # Testcase
    if mode == "testcase":
        msg = await update.message.reply_text("вЏі Р“РµРЅРµСЂРёСЂСѓСЋ С‚РµСЃС‚-РєРµР№СЃС‹ РїРѕ ISTQB...")
        response = await ask_ai(
            f"РќР°РїРёС€Рё РїРѕРґСЂРѕР±РЅС‹Рµ С‚РµСЃС‚-РєРµР№СЃС‹ РїРѕ ISTQB-СЃС‚Р°РЅРґР°СЂС‚Р°Рј РґР»СЏ:\n\n{text}",
            system_override=_TESTCASE_SYSTEM,
        )
        context.user_data.pop("mode", None)
        await msg.delete()
        await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())
        return

    # Bugreport
    if mode == "bugreport":
        msg = await update.message.reply_text("вЏі РЎРѕСЃС‚Р°РІР»СЏСЋ Р±Р°Рі-СЂРµРїРѕСЂС‚...")
        response = await ask_ai(
            f"РЎРѕСЃС‚Р°РІСЊ Р±Р°Рі-СЂРµРїРѕСЂС‚ РїРѕ СЃС‚Р°РЅРґР°СЂС‚Р°Рј:\n\n{text}",
            system_override=_BUGREPORT_SYSTEM,
        )
        context.user_data.pop("mode", None)
        await msg.delete()
        await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())
        return

    # Interview
    if mode == "interview":
        msg = await update.message.reply_text("вЏі Р“РѕС‚РѕРІР»СЋ РІРѕРїСЂРѕСЃС‹ РґР»СЏ СЃРѕР±РµСЃРµРґРѕРІР°РЅРёСЏ...")
        response = await ask_ai(
            f"Р”Р°Р№ С‚РѕРї-5 РІРѕРїСЂРѕСЃРѕРІ РЅР° СЃРѕР±РµСЃРµРґРѕРІР°РЅРёРё РїРѕ С‚РµРјРµ В«{text}В» СЃ СЂР°Р·РІС‘СЂРЅСѓС‚С‹РјРё РѕС‚РІРµС‚Р°РјРё.",
        )
        context.user_data.pop("mode", None)
        await msg.delete()
        await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())
        return

    # Default: general QA question
    msg = await update.message.reply_text("рџ¤” Р”СѓРјР°СЋ...")
    response = await ask_ai(text)
    await msg.delete()
    await update.message.reply_text(response, parse_mode="HTML", reply_markup=kb_main_menu())


# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ
# HELPERS
# в•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђв•ђ

_TESTCASE_SYSTEM = """РўС‹ вЂ” РѕРїС‹С‚РЅС‹Р№ QA-РёРЅР¶РµРЅРµСЂ СЃ 10+ Р»РµС‚Р°РјРё РѕРїС‹С‚Р°.
РЎРѕР·РґР°РІР°Р№ С‚РµСЃС‚-РєРµР№СЃС‹ СЃС‚СЂРѕРіРѕ РїРѕ ISTQB-СЃС‚Р°РЅРґР°СЂС‚Р°Рј:
- ID, РќР°Р·РІР°РЅРёРµ, РџСЂРµРґСѓСЃР»РѕРІРёСЏ, РЁР°РіРё, РћР¶РёРґР°РµРјС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚, РўРёРї (РїРѕР·РёС‚РёРІРЅС‹Р№/РЅРµРіР°С‚РёРІРЅС‹Р№)
- РџСЂРёРјРµРЅСЏР№ BVA, EP, РїРµСЂРµС…РѕРґС‹ СЃРѕСЃС‚РѕСЏРЅРёР№
- РћС‚РІРµС‡Р°Р№ РЅР° СЂСѓСЃСЃРєРѕРј СЏР·С‹РєРµ
- РСЃРїРѕР»СЊР·СѓР№ HTML-С„РѕСЂРјР°С‚РёСЂРѕРІР°РЅРёРµ РґР»СЏ Telegram"""

_BUGREPORT_SYSTEM = """РўС‹ вЂ” РѕРїС‹С‚РЅС‹Р№ QA-РёРЅР¶РµРЅРµСЂ.
РЎРѕСЃС‚Р°РІР»СЏР№ Р±Р°Рі-СЂРµРїРѕСЂС‚С‹ РїРѕ СЃС‚Р°РЅРґР°СЂС‚Р°Рј:
- Р—Р°РіРѕР»РѕРІРѕРє, РЎРµСЂСЊС‘Р·РЅРѕСЃС‚СЊ (severity), РџСЂРёРѕСЂРёС‚РµС‚, РћРєСЂСѓР¶РµРЅРёРµ, РЁР°РіРё РІРѕСЃРїСЂРѕРёР·РІРµРґРµРЅРёСЏ, 
  РћР¶РёРґР°РµРјС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚, Р¤Р°РєС‚РёС‡РµСЃРєРёР№ СЂРµР·СѓР»СЊС‚Р°С‚, Р’Р»РѕР¶РµРЅРёСЏ (С‡С‚Рѕ РїСЂРёР»РѕР¶РёС‚СЊ)
- РћС‚РІРµС‡Р°Р№ РЅР° СЂСѓСЃСЃРєРѕРј СЏР·С‹РєРµ
- РСЃРїРѕР»СЊР·СѓР№ HTML-С„РѕСЂРјР°С‚РёСЂРѕРІР°РЅРёРµ РґР»СЏ Telegram"""


async def _get_theory(topic: str) -> str:
    """Get theory content for a topic."""
    topics = {
        "design": (
            "рџ“ђ <b>РњРµС‚РѕРґС‹ С‚РµСЃС‚-РґРёР·Р°Р№РЅР° (ISTQB CTFL 4.2)</b>\n\n"
            "вЂў <b>Р­РєРІРёРІР°Р»РµРЅС‚РЅРѕРµ СЂР°Р·Р±РёРµРЅРёРµ (EP)</b> вЂ” РґРµР»РёРј РґР°РЅРЅС‹Рµ РЅР° РєР»Р°СЃСЃС‹, С‚РµСЃС‚РёСЂСѓРµРј РїРѕ РѕРґРЅРѕРјСѓ РёР· РєР°Р¶РґРѕРіРѕ\n"
            "вЂў <b>Р“СЂР°РЅРёС‡РЅС‹Рµ Р·РЅР°С‡РµРЅРёСЏ (BVA)</b> вЂ” С‚РµСЃС‚РёСЂСѓРµРј РЅР° РіСЂР°РЅРёС†Р°С… РґРёР°РїР°Р·РѕРЅРѕРІ\n"
            "вЂў <b>РўР°Р±Р»РёС†Р° СЂРµС€РµРЅРёР№</b> вЂ” РєРѕРјР±РёРЅР°С†РёРё СѓСЃР»РѕРІРёР№ Рё РґРµР№СЃС‚РІРёР№\n"
            "вЂў <b>РџРµСЂРµС…РѕРґС‹ СЃРѕСЃС‚РѕСЏРЅРёР№</b> вЂ” РїРѕРІРµРґРµРЅРёРµ РїСЂРё СЃРјРµРЅРµ СЃРѕСЃС‚РѕСЏРЅРёР№\n"
            "вЂў <b>РџРѕРїР°СЂРЅРѕРµ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ (Pairwise)</b> вЂ” РїРѕРєСЂС‹РІР°РµРј РІСЃРµ РїР°СЂС‹ РїР°СЂР°РјРµС‚СЂРѕРІ\n"
            "вЂў <b>РСЃСЃР»РµРґРѕРІР°С‚РµР»СЊСЃРєРѕРµ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ</b> вЂ” РѕР±СѓС‡РµРЅРёРµ + РїСЂРѕРµРєС‚РёСЂРѕРІР°РЅРёРµ + РІС‹РїРѕР»РЅРµРЅРёРµ РѕРґРЅРѕРІСЂРµРјРµРЅРЅРѕ\n\n"
            "рџ’Ў <i>РЎРѕРІРµС‚: РЅР° СЌРєР·Р°РјРµРЅРµ ISTQB С‡Р°СЃС‚Рѕ СЃРїСЂР°С€РёРІР°СЋС‚ Рѕ СЂР°Р·РЅРёС†Рµ EP vs BVA</i>"
        ),
        "levels": (
            "рџ“Љ <b>РЈСЂРѕРІРЅРё С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ (ISTQB CTFL 2.2)</b>\n\n"
            "вЂў <b>РљРѕРјРїРѕРЅРµРЅС‚РЅРѕРµ (Unit)</b> вЂ” РѕС‚РґРµР»СЊРЅС‹Рµ РјРѕРґСѓР»Рё, Р±С‹СЃС‚СЂС‹Рµ, РјРЅРѕРіРѕ\n"
            "вЂў <b>РРЅС‚РµРіСЂР°С†РёРѕРЅРЅРѕРµ</b> вЂ” РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёРµ РєРѕРјРїРѕРЅРµРЅС‚РѕРІ\n"
            "вЂў <b>РЎРёСЃС‚РµРјРЅРѕРµ</b> вЂ” СЃРёСЃС‚РµРјР° С†РµР»РёРєРѕРј РїСЂРѕС‚РёРІ С‚СЂРµР±РѕРІР°РЅРёР№\n"
            "вЂў <b>РџСЂРёС‘РјРѕС‡РЅРѕРµ (UAT)</b> вЂ” С„РёРЅР°Р»СЊРЅР°СЏ РїСЂРѕРІРµСЂРєР° Р±РёР·РЅРµСЃ-С‚СЂРµР±РѕРІР°РЅРёР№\n\n"
            "рџ”є <b>РџРёСЂР°РјРёРґР° С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ:</b> Unit (РѕСЃРЅРѕРІР°РЅРёРµ) в†’ Integration в†’ E2E (РІРµСЂС€РёРЅР°)\n"
            "Р§РµРј РІС‹С€Рµ вЂ” С‚РµРј РјРµРґР»РµРЅРЅРµРµ Рё РґРѕСЂРѕР¶Рµ."
        ),
        "types": (
            "рџ”¬ <b>Р’РёРґС‹ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ</b>\n\n"
            "РџРѕ Р·РЅР°РЅРёСЋ СЃРёСЃС‚РµРјС‹:\n"
            "вЂў <b>Black-box</b> вЂ” Р±РµР· Р·РЅР°РЅРёСЏ РІРЅСѓС‚СЂРµРЅРЅРµР№ СЃС‚СЂСѓРєС‚СѓСЂС‹\n"
            "вЂў <b>White-box</b> вЂ” СЃ РїРѕР»РЅС‹Рј Р·РЅР°РЅРёРµРј РєРѕРґР°\n"
            "вЂў <b>Grey-box</b> вЂ” С‡Р°СЃС‚РёС‡РЅРѕРµ Р·РЅР°РЅРёРµ\n\n"
            "РџРѕ С†РµР»Рё:\n"
            "вЂў <b>Р¤СѓРЅРєС†РёРѕРЅР°Р»СЊРЅРѕРµ</b> вЂ” С‡С‚Рѕ СЃРёСЃС‚РµРјР° РґРµР»Р°РµС‚\n"
            "вЂў <b>РќРµС„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅРѕРµ</b> вЂ” РєР°Рє РґРµР»Р°РµС‚ (РїСЂРѕРёР·РІРѕРґРёС‚РµР»СЊРЅРѕСЃС‚СЊ, Р±РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ)\n"
            "вЂў <b>РЎС‚СЂСѓРєС‚СѓСЂРЅРѕРµ</b> вЂ” РїРѕРєСЂС‹С‚РёРµ РєРѕРґР°\n"
            "вЂў <b>Р РµРіСЂРµСЃСЃРёРѕРЅРЅРѕРµ</b> вЂ” РЅРµ СЃР»РѕРјР°Р»Рё Р»Рё РёР·РјРµРЅРµРЅРёСЏ СЃС‚Р°СЂРѕРµ\n"
            "вЂў <b>Smoke/Sanity</b> вЂ” Р±С‹СЃС‚СЂР°СЏ РїСЂРѕРІРµСЂРєР° Р±Р°Р·РѕРІРѕР№ СЂР°Р±РѕС‚РѕСЃРїРѕСЃРѕР±РЅРѕСЃС‚Рё"
        ),
        "principles": (
            "рџ“‹ <b>7 РїСЂРёРЅС†РёРїРѕРІ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ ISTQB (CTFL 1.3)</b>\n\n"
            "1пёЏвѓЈ <b>РўРµСЃС‚РёСЂРѕРІР°РЅРёРµ РїРѕРєР°Р·С‹РІР°РµС‚ РЅР°Р»РёС‡РёРµ РґРµС„РµРєС‚РѕРІ, Р° РЅРµ РёС… РѕС‚СЃСѓС‚СЃС‚РІРёРµ</b>\n"
            "2пёЏвѓЈ <b>РСЃС‡РµСЂРїС‹РІР°СЋС‰РµРµ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ РЅРµРІРѕР·РјРѕР¶РЅРѕ</b> вЂ” РёСЃРїРѕР»СЊР·СѓР№ BVA, EP\n"
            "3пёЏвѓЈ <b>Р Р°РЅРЅРµРµ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ СЌРєРѕРЅРѕРјРёС‚ РґРµРЅСЊРіРё</b> вЂ” С‡РµРј СЂР°РЅСЊС€Рµ, С‚РµРј РґРµС€РµРІР»Рµ\n"
            "4пёЏвѓЈ <b>РЎРєРѕРїР»РµРЅРёРµ РґРµС„РµРєС‚РѕРІ</b> вЂ” 80% РїСЂРѕР±Р»РµРј РІ 20% РєРѕРґР°\n"
            "5пёЏвѓЈ <b>РџР°СЂР°РґРѕРєСЃ РїРµСЃС‚РёС†РёРґРѕРІ</b> вЂ” С‚Рµ Р¶Рµ С‚РµСЃС‚С‹ РїРµСЂРµСЃС‚Р°СЋС‚ РЅР°С…РѕРґРёС‚СЊ Р±Р°РіРё\n"
            "6пёЏвѓЈ <b>РўРµСЃС‚РёСЂРѕРІР°РЅРёРµ Р·Р°РІРёСЃРёС‚ РѕС‚ РєРѕРЅС‚РµРєСЃС‚Р°</b>\n"
            "7пёЏвѓЈ <b>РћС€РёР±РѕС‡РЅРѕСЃС‚СЊ РѕС‚СЃСѓС‚СЃС‚РІРёСЏ РґРµС„РµРєС‚РѕРІ</b> вЂ” В«РЅРµС‚ Р±Р°РіРѕРІВ» в‰  С…РѕСЂРѕС€РёР№ РїСЂРѕРґСѓРєС‚"
        ),
        "automation": (
            "рџ¤– <b>РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЏ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ</b>\n\n"
            "<b>РљРѕРіРґР° Р°РІС‚РѕРјР°С‚РёР·РёСЂРѕРІР°С‚СЊ:</b>\n"
            "вЂў Р РµРіСЂРµСЃСЃРёРѕРЅРЅС‹Рµ С‚РµСЃС‚С‹\n"
            "вЂў Р§Р°СЃС‚Рѕ РїРѕРІС‚РѕСЂСЏСЋС‰РёРµСЃСЏ СЃС†РµРЅР°СЂРёРё\n"
            "вЂў РќР°РіСЂСѓР·РѕС‡РЅРѕРµ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ\n\n"
            "<b>РџРѕРїСѓР»СЏСЂРЅС‹Рµ РёРЅСЃС‚СЂСѓРјРµРЅС‚С‹:</b>\n"
            "вЂў <b>Selenium/Playwright</b> вЂ” UI-С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ\n"
            "вЂў <b>Postman/RestAssured</b> вЂ” API-С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ\n"
            "вЂў <b>JUnit/PyTest</b> вЂ” unit-С‚РµСЃС‚С‹\n"
            "вЂў <b>Appium</b> вЂ” РјРѕР±РёР»СЊРЅР°СЏ Р°РІС‚РѕРјР°С‚РёР·Р°С†РёСЏ\n"
            "вЂў <b>k6/JMeter</b> вЂ” РЅР°РіСЂСѓР·РѕС‡РЅРѕРµ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ\n\n"
            "вљ пёЏ <i>РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЏ в‰  Р·Р°РјРµРЅР° СЂСѓС‡РЅРѕРіРѕ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ. Р”РѕРїРѕР»РЅСЏРµС‚ РµРіРѕ!</i>"
        ),
        "mobile": (
            "рџ“± <b>Mobile С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ (ISTQB Mobile Tester)</b>\n\n"
            "<b>РўРёРїС‹ РїСЂРёР»РѕР¶РµРЅРёР№:</b>\n"
            "вЂў <b>Native</b> вЂ” Swift/ObjC (iOS), Kotlin/Java (Android)\n"
            "вЂў <b>Web-based</b> вЂ” Р±СЂР°СѓР·РµСЂРЅС‹Рµ, HTML/CSS/JS\n"
            "вЂў <b>Hybrid</b> вЂ” РЅР°С‚РёРІРЅР°СЏ РѕР±С‘СЂС‚РєР° + РІРµР±-РєРѕРЅС‚РµРЅС‚\n\n"
            "<b>РћСЃРѕР±РµРЅРЅРѕСЃС‚Рё С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ:</b>\n"
            "вЂў Р Р°Р·РЅС‹Рµ СЂР°Р·РјРµСЂС‹ СЌРєСЂР°РЅРѕРІ Рё СЂР°Р·СЂРµС€РµРЅРёСЏ\n"
            "вЂў РќРµСЃС‚Р°Р±РёР»СЊРЅР°СЏ СЃРµС‚СЊ (3G/4G/WiFi)\n"
            "вЂў Р Р°Р·РЅС‹Рµ РІРµСЂСЃРёРё РћРЎ (iOS 14/15/16, Android 10/11/12)\n"
            "вЂў РџСЂРµСЂС‹РІР°РЅРёСЏ: Р·РІРѕРЅРєРё, СѓРІРµРґРѕРјР»РµРЅРёСЏ, РЅРёР·РєРёР№ Р·Р°СЂСЏРґ\n"
            "вЂў Р Р°Р·СЂРµС€РµРЅРёСЏ РїСЂРёР»РѕР¶РµРЅРёСЏ (РєР°РјРµСЂР°, РіРµРѕР»РѕРєР°С†РёСЏ)\n\n"
            "<b>Р­РјСѓР»СЏС‚РѕСЂ vs РЎРёРјСѓР»СЏС‚РѕСЂ:</b>\n"
            "вЂў Р­РјСѓР»СЏС‚РѕСЂ вЂ” РёРјРёС‚РёСЂСѓРµС‚ hardware + software (Android Emulator)\n"
            "вЂў РЎРёРјСѓР»СЏС‚РѕСЂ вЂ” С‚РѕР»СЊРєРѕ software (iOS Simulator)"
        ),
    }
    return topics.get(topic, "РўРµРјР° РЅРµ РЅР°Р№РґРµРЅР°. Р’С‹Р±РµСЂРё РґСЂСѓРіСѓСЋ.")


async def _send_tools(reply_fn) -> None:
    text = (
        "рџ›  <b>РРЅСЃС‚СЂСѓРјРµРЅС‚С‹ QA</b>\n\n"
        "<b>рџ“ќ РЈРїСЂР°РІР»РµРЅРёРµ С‚РµСЃС‚Р°РјРё:</b>\n"
        "вЂў <a href='https://testlink.org'>TestLink</a> вЂ” open source TMS\n"
        "вЂў <a href='https://www.testrail.com'>TestRail</a> вЂ” РїРѕРїСѓР»СЏСЂРЅС‹Р№ TMS\n"
        "вЂў <a href='https://qase.io'>Qase</a> вЂ” СЃРѕРІСЂРµРјРµРЅРЅС‹Р№ TMS\n\n"
        "<b>рџђ› Р‘Р°Рі-С‚СЂРµРєРµСЂС‹:</b>\n"
        "вЂў <a href='https://www.atlassian.com/software/jira'>Jira</a> вЂ” СЃС‚Р°РЅРґР°СЂС‚ РёРЅРґСѓСЃС‚СЂРёРё\n"
        "вЂў <a href='https://www.youtrack.com'>YouTrack</a> вЂ” РѕС‚ JetBrains\n"
        "вЂў <a href='https://github.com'>GitHub Issues</a> вЂ” РґР»СЏ СЂР°Р·СЂР°Р±РѕС‚С‡РёРєРѕРІ\n\n"
        "<b>рџ¤– РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЏ:</b>\n"
        "вЂў <a href='https://www.selenium.dev'>Selenium</a> вЂ” UI-Р°РІС‚РѕРјР°С‚РёР·Р°С†РёСЏ\n"
        "вЂў <a href='https://playwright.dev'>Playwright</a> вЂ” СЃРѕРІСЂРµРјРµРЅРЅР°СЏ Р°Р»СЊС‚РµСЂРЅР°С‚РёРІР°\n"
        "вЂў <a href='https://appium.io'>Appium</a> вЂ” РјРѕР±РёР»СЊРЅР°СЏ Р°РІС‚РѕРјР°С‚РёР·Р°С†РёСЏ\n"
        "вЂў <a href='https://www.postman.com'>Postman</a> вЂ” API-С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ\n\n"
        "<b>вљЎ РќР°РіСЂСѓР·РѕС‡РЅРѕРµ С‚РµСЃС‚РёСЂРѕРІР°РЅРёРµ:</b>\n"
        "вЂў <a href='https://k6.io'>k6</a> вЂ” СЃРѕРІСЂРµРјРµРЅРЅС‹Р№ РёРЅСЃС‚СЂСѓРјРµРЅС‚\n"
        "вЂў <a href='https://jmeter.apache.org'>JMeter</a> вЂ” РєР»Р°СЃСЃРёС‡РµСЃРєРёР№ РІС‹Р±РѕСЂ"
    )
    await reply_fn(text, parse_mode="HTML", reply_markup=kb_back_to_menu(),
                   disable_web_page_preview=True)


def register_handlers(app: Application) -> None:
    """Register all handlers with the application."""
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

