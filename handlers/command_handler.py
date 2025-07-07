from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send any football content — I’ll translate, rewrite, and post it professionally!")

start_command = CommandHandler("start", start)
