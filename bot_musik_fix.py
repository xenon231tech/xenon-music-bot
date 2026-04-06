import os
import yt_dlp
from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters

TOKEN = "8662818192:AAGg83V4jBvpUJR9rnpUXYOquHmLn7m7cgA"

# Data premium user
premium_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ *XENON MUSIC BOT* ⚡\n\n"
        "Send /play [song title] to play music from YouTube!\n\n"
        "📌 Example: /play st12 saat terakhir\n\n"
        "✨ Type /premium to get lifetime access!",
        parse_mode='Markdown'
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Example: /play st12 saat terakhir")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Searching: {query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        os.makedirs('downloads', exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            entry = info['entries'][0]
            title = entry['title']
            base_filename = ydl.prepare_filename(entry).rsplit('.', 1)[0]
            audio_file = f"{base_filename}.mp3"

        with open(audio_file, 'rb') as audio:
            await update.message.reply_audio(audio=audio, title=title, performer="YouTube")

        os.remove(audio_file)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏹️ Playback stopped.")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ *XENON MUSIC BOT v1.0* ⚡\n\n"
        "Built with Python & yt-dlp\n\n"
        "💎 *Features:*\n"
        "• YouTube audio streaming\n"
        "• Auto-download & cleanup\n"
        "• Premium features available\n\n"
        "🚀 Powered by Xenon Labs",
        parse_mode='Markdown'
    )

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_invoice(
        title="✨ XENON MUSIC PREMIUM ✨",
        description="Get lifetime access to premium features:\n\n✅ Unlimited playlists\n✅ MP3 downloads\n✅ High quality audio",
        payload="premium_v1",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Premium Lifetime", amount=50)],
    )

async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    premium_users[user_id] = True
    await update.message.reply_text(
        "✅ *PAYMENT SUCCESSFUL!*\n\n"
        "You are now a XENON MUSIC PREMIUM user!\n\n"
        "Thank you for supporting this bot! 🙏",
        parse_mode='Markdown'
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    print("✅ XENON MUSIC BOT is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
