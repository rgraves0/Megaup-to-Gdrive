import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Drive API အတွက် SCOPES
SCOPES = ['https://www.googleapis.com/auth/drive.file']

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

if __name__ == "__main__":
    # Google Drive API အတွက် authentication လုပ်ပါ
    drive_service = get_drive_service()
    print("Authentication successful! token.json has been generated.")