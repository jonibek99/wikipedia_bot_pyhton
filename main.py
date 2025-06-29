from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import wikipedia
from dotenv import load_dotenv
import os
from tinydb import TinyDB,Query
import json
wikipedia.set_lang('uz')
load_dotenv()
token = os.getenv("token")

updater = Updater(token=token)
dispatcher = updater.dispatcher
db1=TinyDB('user_info.json')
bd2=TinyDB('user_datas.json')
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user=update.message.from_user
    update.message.reply_text("Salom! Menga biror mavzu yozing, men Wikipedia'dan topib beraman.")
    global db1
    a=Query()
    if not db1.search(a.chat_id==chat_id):
        db1.insert({
            'chat_id':chat_id,
            'first_name':user.first_name,
            'last_name':user.last_name

        })
def wiki_search(update:Update,context:CallbackContext):
    global bd2
    bot=context.bot
    a=Query()
    chat_id=update.message.chat.id
    text=update.message.text.strip().lower().capitalize()
    user_info=update.message.from_user
    try:
        results=wikipedia.search(text)
        if results:
         buttons = [[InlineKeyboardButton(text=title, callback_data=f"wiki_{title}")]for title in results[:]]
         reply_markup = InlineKeyboardMarkup(buttons)
         bot.send_message(chat_id=chat_id,
                text='quyidagi maqoladan bitini tanlang',
                reply_markup=reply_markup)
        else:
            bot.send_message(chat_id=chat_id, text="❌ Ma'lumot topilmadi.")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text="xatolik yuz berdi {e}")
        a=Query()
        # if not bd2.search(a.chat_id==chat_id):
        #     bd2.update({chat_id:chat_id,
        #                 first_name:user_info.first_name,
        #                 last_name:user_info.last_name,
        #                 query:text,
        #                 title:


        #     })
def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data.startswith("wiki_"):
        topic = data.replace("wiki_", "")

        try:
            summary = wikipedia.summary(topic, sentences=3)
            query.message.reply_text(f"📘 *{topic}*\n\n{summary}", parse_mode='Markdown')
        except Exception as e:
            query.message.reply_text(f"⚠️ Xatolik: {e}")

    query.answer() 


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, wiki_search))
dispatcher.add_handler(CallbackQueryHandler(handle_callback))
updater.start_polling()
print('🤖 bot started working')
updater.idle()



