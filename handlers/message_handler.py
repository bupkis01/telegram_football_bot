import re
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from services.translator import translate_to_english
from services.rewriter import rewrite_professionally
from services.journalist_verifier import extract_and_translate_name
from utils.text_utils import escape_html
from utils.rate_limiter import is_rate_limited
from config import TELEGRAM_CHANNEL

logger = logging.getLogger(__name__)

def clean_and_format(rewritten: str, source: str, channel: str) -> str:
    """
    Cleans the AI-rewritten text by removing any leading 🚨📢 name: prefix,
    then formats the message with a single 🚨 emoji, the cleaned text,
    source attribution, and channel tag.
    """
    # Remove any leading "🚨📢 Name: " or similar prefix
    cleaned = re.sub(r"^[^:]{2,40}:\s*", "", rewritten.strip())
    return (
        f"🚨 {escape_html(cleaned)}\n\n"
        f"Source : {escape_html(source)}\n"
        f"{channel}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message:
        return

    user_id = update.effective_user.id
    if is_rate_limited(user_id):
        await message.reply_text("⏳ You're sending too fast. Please wait.")
        return

    text = message.caption or message.text
    if not text:
        await message.reply_text("📷 Please include a caption or text with your media.")
        return

    await message.reply_text("🌐 Translating...")
    english_text = await translate_to_english(text)

    await message.reply_text("✍️ Rewriting professionally...")
    rewritten = await rewrite_professionally(english_text)

    # ✅ Automatically extract + translate speaker's name
    source = await extract_and_translate_name(text)
    if not source:
        source = "Unknown"

    # 🧼 Final clean format
    final_text = clean_and_format(rewritten, source, "@FootballEdge0")

    try:
        if message.photo:
            await context.bot.send_photo(
                chat_id=TELEGRAM_CHANNEL,
                photo=message.photo[-1].file_id,
                caption=final_text,
                parse_mode="HTML"
            )
        elif message.video:
            await context.bot.send_video(
                chat_id=TELEGRAM_CHANNEL,
                video=message.video.file_id,
                caption=final_text,
                parse_mode="HTML"
            )
        else:
            await context.bot.send_message(
                chat_id=TELEGRAM_CHANNEL,
                text=final_text,
                parse_mode="HTML"
            )
        await message.reply_text("✅ Posted to channel.")
    except Exception as e:
        logger.error(f"Error posting to channel: {e}")
        await message.reply_text("⚠️ Error while posting to channel.")

# ✅ Register this message handler in main.py
message_handler = MessageHandler(filters.ALL, handle_message)
