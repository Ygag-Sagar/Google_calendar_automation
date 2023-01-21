import pickle
from decouple import config
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from constant import AUTH_URI, AUTH_PROVIDER, TOKEN_URI, REDIRECT_URIS

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
# CREDENTIALS_FILE = './google-credentials.json'
# CRED = config('CR')
# CREDENTIALS = json.loads(CRED)

CREDENTIALS = {
    "installed": {
        "client_id": config('CLIENT_ID'),
        "project_id": config('PROJECT_ID'),
        "auth_uri": AUTH_URI,
        "token_uri": TOKEN_URI,
        "auth_provider_x509_cert_url": AUTH_PROVIDER,
        "client_secret": config('CLIENT_SECRET'),
        "redirect_uris": [
            REDIRECT_URIS
        ]
    }
}


def get_calendar_service():
    creds = None

    ''' The file token.pickle stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.'''

    if os.path.exists('tokkkkkk.pickle'):  # Check the existence of the file token.pickle.
        with open('tokkkkkk.pickle', 'rb') as token:  # If it does, open the file as rb (binary format for reading).
            creds = pickle.load(token)  # Assign the content of the token into creds.

    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:  # Check weather the creds is available, or it is valid.
        if creds and creds.expired and creds.refresh_token:  # If there's creds and creds is expired and there's \
            # a refresh token as well.
            creds.refresh(Request())  # Send a request for new token
        else:
            flow = InstalledAppFlow.from_client_config( #from_client_secrets_file from_client_config
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('tokkkkkk.pickle', 'wb') as token:
            pickle.dump(creds, token)
            # token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service
