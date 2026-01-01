import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USERS = [968936791]  # your Telegram ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ You are not allowed to use this bot.")
        return

    await update.message.reply_text(
        "✅ Bot is running!\n\n"
        "Send an Instagram link to download media."
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set in environment variables")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot started successfully...")
    app.run_polling()


if __name__ == "__main__":
    main()
