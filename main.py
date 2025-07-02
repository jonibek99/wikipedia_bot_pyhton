from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    InlineQueryHandler,
)
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
import wikipedia
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query
import json

wikipedia.set_lang("uz")
load_dotenv()
token = os.getenv("token")

updater = Updater(token=token)
dispatcher = updater.dispatcher
db1 = TinyDB("user_info.json")
bd2 = TinyDB("user_datas.json")


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user = update.message.from_user
    update.message.reply_text(
        "Salom! Menga biror mavzu yozing, men Wikipedia'dan topib beraman."
    )
    global db1
    a = Query()
    if not db1.search(a.chat_id == chat_id):
        db1.insert(
            {
                "chat_id": chat_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )


def handle_callback(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        summary = wikipedia.summary(text, sentences=3)
        update.effective_message.reply_text(
            f"📘 *{text}*\n\n{summary}", parse_mode="Markdown"
        )
    except Exception as e:
        update.effective_message.reply_text(f"⚠️ Xatolik: {e}")


def test(update: Update, context: CallbackContext):
    query = update.inline_query.query
    results = wikipedia.search(query)
    print(results)
    if len(results) == 0:
        update.inline_query.answer(
            results=[],
            switch_pm_text="Ma'lumot topilmadi",
            switch_pm_parameter="no_results",
        )
        return
    update.inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id=str(i),
                title=results[i],
                input_message_content=InputTextMessageContent(message_text=results[i]),
            )
            for i in range(len(results[:40]))
        ],
    )


def chosen(update: Update, context: CallbackContext):
    print("Chosen inline result received")
    result = update.chosen_inline_result
    print(f"Chosen result: {result.result_id}")
    print(f"User: {result.from_user.first_name}")
    print(f"Query: {result.query}")


dispatcher.add_handler(InlineQueryHandler(test))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_callback))
updater.start_polling()
print("🤖 bot started working")
updater.idle()
