import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from services.translator import translate_to_english
from services.rewriter import rewrite_professionally
from services.journalist_verifier import is_trusted_journalist_from_text
from utils.text_utils import escape_html
from utils.rate_limiter import is_rate_limited
from config import TELEGRAM_CHANNEL

logger = logging.getLogger(__name__)

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

    # ✅ Automatically detect journalist using AI
    source = await is_trusted_journalist_from_text(english_text) or ""

    # 🧼 Clean output for Telegram (escape special characters)
    safe_rewritten = escape_html(rewritten)
    safe_source = escape_html(source)

    final_text = f"🚨📢 {safe_rewritten}"
    if source:
        final_text += f"\n\n📎 Source : {safe_source}\n🔁 @FootballEdge0"
    else:
        final_text += "\n\n🔁 @FootballEdge0"

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
