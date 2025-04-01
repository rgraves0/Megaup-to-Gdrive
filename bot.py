import os
import urllib.parse
import requests
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext import filters
from aiohttp import web
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API အတွက် SCOPES
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Telegram Bot Token ကို environment variable ကနေ ဖတ်ပါမယ်
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")

# Bot ကို ဖန်တီးပါ
app = Application.builder().token(BOT_TOKEN).build()

# Google Drive Service ကို ဖန်တီးဖို့ function
def get_drive_service():
    creds = None
    # token.json ဖိုင်ကနေ credentials ကို ဖတ်ပါ
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # အကယ်၍ credentials မရှိရင် သို့မဟုတ် မမှန်ကန်ရင် အသစ်ဖန်တီးပါ
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # ဖန်တီးထားတဲ့ credentials ကို token.json ဖိုင်ထဲ သိမ်းပါ
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

# Google Drive ထဲ ဖိုင်အပ်လုဒ်လုပ်ဖို့ function
def upload_to_drive(file_path, file_name):
    try:
        drive_service = get_drive_service()
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        print(f"Error uploading to Google Drive: {str(e)}")
        return None

# Start command handler
async def start(update, context):
    await update.message.reply_text("Hello! Please send me a MegaUp direct download link, and I'll upload it to your Google Drive.")

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
                await update.message.reply_text(f"File downloaded successfully: {file_name}. Uploading to Google Drive...")

                # Upload to Google Drive
                file_id = upload_to_drive(save_path, file_name)
                if file_id:
                    file_url = f"https://drive.google.com/file/d/{file_id}/view"
                    await update.message.reply_text(f"File uploaded to Google Drive: {file_url}")
                else:
                    await update.message.reply_text("Failed to upload to Google Drive.")
                
                # Delete the local file after uploading
                os.remove(save_path)
            else:
                await update.message.reply_text("Download failed: File not found.")
        except Exception as e:
            await update.message.reply_text(f"Error occurred: {str(e)}")
    else:
        await update.message.reply_text("Please send a valid MegaUp direct download link.")

# Add handlers to the application
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text() & ~filters.Command(), handle_message))

# Webhook handler for Railway.app
async def webhook(request):
    try:
        update = telegram.Update.de_json(await request.json(), app.bot)
        if update:
            await app.process_update(update)
        return web.Response(text="OK")
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        return web.Response(text="Error", status=500)

# Set up the webhook server
async def main():
    # Set webhook
    webhook_url = f"{RAILWAY_URL}/{BOT_TOKEN}"
    await app.bot.set_webhook(url=webhook_url)
    print(f"Webhook set to: {webhook_url}")

    # Start the webhook server
    port = int(os.getenv("PORT", 8080))  # Railway.app မှာ PORT ကို သတ်မှတ်ထားရင် အဲဒီ port ကို သုံးမယ်
    web_app = web.Application()
    web_app.router.add_post(f"/{BOT_TOKEN}", webhook)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"Bot is running with webhook on port {port}...")

    # Keep the application running
    await app.initialize()
    await app.start()
    # Run forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
