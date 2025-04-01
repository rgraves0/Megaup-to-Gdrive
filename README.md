# Telegram MegaUp to Google Drive Bot

This is a Telegram bot that allows you to download files from MegaUp links and upload them directly to your Google Drive. The bot is deployed on Railway.app and uses the Google Drive API for file uploads.

## Features
- Download files from MegaUp direct download links.
- Upload the downloaded files to your Google Drive.
- Get a shareable Google Drive link after the upload.
- Simple and easy-to-use Telegram interface.

## Prerequisites
Before setting up the bot, ensure you have the following:
- A Telegram account and a bot token from [BotFather](https://t.me/BotFather).
- A Google Cloud Console project with the Google Drive API enabled.
- A `credentials.json` file from Google Cloud Console for Google Drive API authentication.
- A Railway.app account for deployment (or any other hosting platform).

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/telegram-megaup-bot.git
cd telegram-megaup-bot

## 2. Install Dependencies
Install the required Python packages listed in requirements.txt:

pip install -r requirements.txt

3. Set Up Google Drive API
Go to the Google Cloud Console.
Create a new project (or use an existing one).
Enable the Google Drive API for your project.
Go to APIs & Services > Credentials, and create an OAuth 2.0 Client ID.
Set the application type to Desktop app.
Download the credentials.json file and place it in the root directory of this project.
Run the generate_token.py script to generate a token.json file:

python generate_token.py

Follow the on-screen instructions to authenticate and generate the token.json file.
Note: Do not upload credentials.json or token.json to GitHub. These files are already ignored in .gitignore.

4. Create a Telegram Bot
Open Telegram and search for BotFather.
Start a chat with BotFather and send the /newbot command.
Follow the instructions to create a new bot and get your Bot Token (e.g., 7324430097:AAG57oZApiBdJOQWsZvkY2BVQI4PUpQ3OAU).
Save the bot token for the next step.
5. Deploy the Bot on Railway.app
Push the Code to GitHub:
If you haven't already, push your local repository to GitHub:

git add .
git commit -m "Initial commit"
git push origin main

Ensure token.json is in your repository (but not credentials.json).

Set Up Railway.app:

Go to Railway.app and sign in.
Create a new project and link it to your GitHub repository.
Once the project is created, go to the "Variables" tab and add the following environment variables:
TELEGRAM_BOT_TOKEN: Your Telegram bot token (e.g., TELEGRAM_BOT_TOKEN).
RAILWAY_URL: The URL of your Railway app (e.g., https://your-app-name.up.railway.app).
Railway.app will automatically deploy your bot. Check the "Logs" tab to ensure the bot is running:

Webhook set to: https://your-app-name.up.railway.app/your-bot-token
Bot is running with webhook on port 8080...

. Test the Bot
Open Telegram and search for your bot (e.g., @YourBotName).
Start the bot by sending the /start command.
Send a MegaUp direct download link (e.g., https://megaup.net/1a2b3c/sample-file.mp4).
The bot will download the file and upload it to your Google Drive, then provide a shareable Google Drive link:

File uploaded to Google Drive: https://drive.google.com/file/d/abc123xyz/view

Usage
Start the Bot: Send /start to the bot to get a welcome message.
Send a MegaUp Link: Send a valid MegaUp direct download link to the bot.
Receive Google Drive Link: The bot will download the file, upload it to your Google Drive, and send you a shareable link.
Folder Configuration (Optional)
By default, files are uploaded to the root directory of your Google Drive. If you want to upload files to a specific folder:

Create a folder in your Google Drive (e.g., MegaUpFiles).
Copy the folder ID from the URL (e.g., https://drive.google.com/drive/folders/abc123xyz → Folder ID is abc123xyz).
Open bot.py and modify the upload_to_drive function:

folder_id = "abc123xyz"  # Replace with your folder ID
file_metadata = {
    'name': file_name,
    'parents': [folder_id]
}

Push the changes to GitHub and redeploy on Railway.app.
Troubleshooting
Bot Not Responding: Check the Railway.app logs for errors. Ensure the TELEGRAM_BOT_TOKEN and RAILWAY_URL variables are set correctly.
Google Drive Upload Fails: Verify that token.json is valid and has the correct permissions. You may need to regenerate it using generate_token.py.
File Download Fails: Ensure the MegaUp link is a direct download link and is accessible.
Contributing
Feel free to fork this repository, make improvements, and submit a pull request. If you encounter any issues, please open an issue on GitHub.

License
This project is licensed under the MIT License. See the  file for details.

Contact
If you have any questions or need help, feel free to reach out via GitHub issues.


---

### **How to Add This to Your GitHub Repository**
1. **Go to Your Repository:**
   - Open your GitHub repository (e.g., `telegram-megaup-bot`).

2. **Create or Edit README.md:**
   - If you don’t have a `README.md` file yet, click on "Create new file" and name it `README.md`.
   - If you already have a `README.md` file, click on it and then click the pencil icon (✏️) to edit.

3. **Copy-Paste the Content:**
   - Copy the entire content above (starting from `# Telegram MegaUp to Google Drive Bot`).
   - Paste it into the `README.md` file on GitHub.

4. **Commit the Changes:**
   - Scroll down to the "Commit changes" section.
   - Add a commit message like `Add README with setup instructions`.
   - Click the "Commit new file" or "Commit changes" button.

---

### **Notes**
- **Replace Placeholders:** Make sure to replace `your-username` in the `git clone` URL with your actual GitHub username. Also, update any example URLs or bot tokens if needed.
- **License File:** The README mentions a `LICENSE` file. If you want to add a license, you can create a `LICENSE` file in your repository and add the MIT License (or any other license you prefer).
- **Screenshots (Optional):** If you want to make the README more visual, you can add screenshots (e.g., of the bot in action on Telegram) by uploading images to your repository and linking them in the README.

Let me know if you need any further adjustments! 😊
