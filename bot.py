import os
import urllib.parse
import requests
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, Filters

# Telegram Bot Token ကို environment variable ကနေ ဖတ်ပါမယ်
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Bot ကို ဖန်တီးပါ
app = Application.builder().token(BOT_TOKEN).build()

# Start command handler
async def start(update, context):
    await update.message.reply_text("Hello! Please send me a MegaUp direct download link, and I'll download it to your local storage.")

# Message handler to process MegaUp links
async def handle_message(update, context):
    message_text = update.message.text

    # Check if the message is a URL
    if "megaup.net" in message_text:
        await update.message.reply_text("Received your MegaUp link! Downloading...")

        # Extract the original file name from the URL
        parsed_url = urllib.parse.urlparse(message_text)
        file_name = os.path.basename(parsed_url.path)
        file_name = urllib.parse.unquote(file_name)

        # Define the path where the file will be saved (local storage)
        save_path = f"./downloads/{file_name}"

        # Create the downloads folder if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Download the file
        try:
            os.system(f'wget -O "{save_path}" "{message_text}"')
            if os.path.exists(save_path):
                await update.message.reply_text(f"File downloaded successfully: {file_name}")
            else:
                await update.message.reply_text("Download failed: File not found.")
        except Exception as e:
            await update.message.reply_text(f"Error occurred: {str(e)}")
    else:
        await update.message.reply_text("Please send a valid MegaUp direct download link.")

# Add handlers to the application
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Set up webhook
async def set_webhook():
    railway_url = os.getenv("RAILWAY_URL")  # Railway.app က ပေးတဲ့ URL
    webhook_url = f"{railway_url}/{BOT_TOKEN}"
    await app.bot.set_webhook(url=webhook_url)

# Run the bot with webhook
if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    print("Bot is running with webhook...")