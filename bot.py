import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================

BOT_TOKEN = os.getenv("BOT_TOKEN")  # set in Render
OWNER_ID = 968936791  # your Telegram ID

# ================= FLASK SERVER =================

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Telegram Bot is running"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# ================= BOT HANDLERS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Access denied")
        return

    await update.message.reply_text(
        "✅ Bot is active\n\n"
        "Send me:\n"
        "• Instagram link\n"
        "• Video link\n"
        "• Any text\n\n"
        "I will process it."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    text = update.message.text
    await update.message.reply_text(f"📩 Received:\n{text}")

# ================= MAIN =================

def main():
    threading.Thread(target=run_flask, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot started successfully")
    app.run_polling()

if __name__ == "__main__":
    main()        "✅ Bot is active\n\n"
        "Send me:\n"
        "• Instagram link\n"
        "• Video link\n"
        "• Any text\n\n"
        "I will process it."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    text = update.message.text
    await update.message.reply_text(f"📩 Received:\n{text}")

# ================= MAIN =================

def main():
    threading.Thread(target=run_flask, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot started successfully")
    app.run_polling()

if __name__ == "__main__":
    main()
