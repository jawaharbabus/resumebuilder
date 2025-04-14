import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = sender_email = os.getenv("SAMPLE_SPREADSHEET_ID")
app_password = sender_email = os.getenv("SAMPLE_RANGE_NAME")
SAMPLE_RANGE_NAME = "jobs"


class GSheets:
    def __init__(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.service = build("sheets", "v4", credentials=creds)
            self.sheet = self.service.spreadsheets()
        except Exception as e:  
            print(e)
        
    def get_values(self, row_to_be_appended):
        list = [str(datetime.today().strftime("%d/%m/%Y"))]+row_to_be_appended+["applied","Jawahar"]
        print(list)
        resource = {
        "majorDimension": "ROWS",
        "values": [list]
        }
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                body=resource,
                valueInputOption="USER_ENTERED"
                ).execute()
        except HttpError as err:
            print(err)
        

# if __name__ == "__main__":
#     gs = GSheets()
#     gs.get_values(["xyz","software","general"])