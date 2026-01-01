import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 968936791  # your Telegram ID
# ----------------------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --------- ACCESS CONTROL ----------
async def check_user(update: Update) -> bool:
    return update.effective_user.id == OWNER_ID

# --------- COMMANDS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_user(update):
        return

    await update.message.reply_text(
        "✅ Instabot is running!\n\n"
        "Send an Instagram link to download media."
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_user(update):
        return

    await update.message.reply_text("🏓 Pong! Bot is alive.")

# --------- MAIN ----------
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    print("🤖 Bot started (Python 3.13 compatible)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
