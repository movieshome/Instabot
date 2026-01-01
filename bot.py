import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")

AUTHORIZED_USER_ID = 968936791  # your Telegram ID

# ---------------- LOGGING ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------- HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized access")
        return

    await update.message.reply_text(
        "✅ Instagram Downloader Bot is running\n\n"
        "Send an Instagram link (post / reel / story)."
    )

# ---------------- MAIN ----------------
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    logger.info("Bot started successfully")

    # 🔥 THIS IS THE IMPORTANT PART 🔥
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
