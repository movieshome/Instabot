import os
import re
import instaloader
from moviepy import VideoFileClip
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# =====================
# CONFIG
# =====================
BOT_TOKEN = "8501654947:AAHagKJG4LqM-YgKudEVBsGgMxvwfYWh-yo"
ALLOWED_USERS = [968936791]   # Your Telegram user ID only

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# =====================
# INSTALOADER SETUP
# =====================
L = instaloader.Instaloader(
    download_pictures=True,
    download_videos=True,
    download_video_thumbnails=False,
    download_comments=False,
    save_metadata=False,
    dirname_pattern=DOWNLOAD_DIR + "/{target}"
)

# =====================
# HELPERS
# =====================
def extract_shortcode(url):
    match = re.search(r"(?:/p/|/reel/|/tv/)([^/?]+)", url)
    return match.group(1) if match else None

# =====================
# START HANDLER
# =====================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        return

    text = update.message.text
    if "instagram.com" not in text:
        await update.message.reply_text("❌ Send a valid Instagram link")
        return

    shortcode = extract_shortcode(text)
    if not shortcode:
        await update.message.reply_text("❌ Unsupported link")
        return

    context.user_data["shortcode"] = shortcode

    keyboard = [
        [InlineKeyboardButton("📷 Download Photos", callback_data="photos")],
        [InlineKeyboardButton("🎥 Download Videos", callback_data="videos")],
        [InlineKeyboardButton("🎵 Audio Only", callback_data="audio")],
        [InlineKeyboardButton("🧾 Caption + Hashtags", callback_data="caption")],
        [InlineKeyboardButton("📖 Download Story", callback_data="story")]
    ]

    await update.message.reply_text(
        "Select download option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =====================
# BUTTON HANDLER
# =====================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    shortcode = context.user_data.get("shortcode")
    if not shortcode:
        await query.edit_message_text("❌ Session expired")
        return

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        target = f"{DOWNLOAD_DIR}/{shortcode}"
        L.download_post(post, target=shortcode)

        files = os.listdir(target)

        # -----------------
        if query.data == "photos":
            for f in files:
                if f.endswith(".jpg"):
                    await query.message.reply_photo(open(f"{target}/{f}", "rb"))

        # -----------------
        elif query.data == "videos":
            for f in files:
                if f.endswith(".mp4"):
                    await query.message.reply_video(open(f"{target}/{f}", "rb"))

        # -----------------
        elif query.data == "audio":
            for f in files:
                if f.endswith(".mp4"):
                    video = VideoFileClip(f"{target}/{f}")
                    audio_path = f"{target}/audio.mp3"
                    video.audio.write_audiofile(audio_path)
                    await query.message.reply_audio(open(audio_path, "rb"))
                    break

        # -----------------
        elif query.data == "caption":
            caption = post.caption or "No caption"
            await query.message.reply_text(caption)

        # -----------------
        elif query.data == "story":
            await query.message.reply_text(
                "⚠️ Story download requires Instagram login.\n"
                "I can add it if you want."
            )

        await query.message.reply_text("✅ Done")

    except Exception as e:
        await query.message.reply_text("❌ Failed (private post or login required)")

# =====================
# MAIN
# =====================
from telegram.ext import ApplicationBuilder

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started successfully")
    app.run_polling()

if __name__ == "__main__":
    main()
