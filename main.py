import asyncio
from telegram.ext import ApplicationBuilder
from config import TELEGRAM_BOT_TOKEN
from handlers.message_handler import message_handler
from handlers.command_handler import start_command

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(start_command)
    app.add_handler(message_handler)
    print("🤖 Bot started...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        import nest_asyncio
        if "event loop is running" in str(e):
            nest_asyncio.apply()
            asyncio.get_event_loop().run_until_complete(main())
        else:
            raise
