import dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, CallbackContext

from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu,
                  default_callback_handler, load_prompt, send_text_buttons)
import  dotenv
import os
dotenv.load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Головне меню',
        'random': 'Дізнатися випадковий цікавий факт 🧠',
        'gpt': 'Задати питання чату GPT 🤖',
        'talk': 'Поговорити з відомою особистістю 👤',
        'quiz': 'Взяти участь у квізі ❓'
        # Додати команду в меню можна так:
        # 'command': 'button text'

    })
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    promt = load_prompt('random')
    await send_image(update, context, 'random')
    response = await chat_gpt.send_question(promt,"Дай рандомний факт")
    await send_text_buttons(update, context, response,{"random_finish":"Закінчити","random_more":"Хочу ще"}
)
async def random_buttons_handler(update: Update, context):
    query = update.callback_query.data
    if query == "random_finish":
        await  start(update, context)
    elif query == "random_more":
        await random(update, context)
    await update.callback_query.answer()

chat_gpt = ChatGptService(os.environ["CHATGPT_TOKEN"])
app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
# Зареєструвати обробник команди можна так:
# app.add_handler(CommandHandler('command', handler_func))

# Зареєструвати обробник колбеку можна так:
app.add_handler(CallbackQueryHandler(random_buttons_handler, pattern='^random_.*'))
# app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
