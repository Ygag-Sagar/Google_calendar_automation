import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import ast

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# CREDENTIALS_FILE = './google-credentials.json'
CREDENTIALS_FILE = './ygag-credentials.json'


def get_calendar_service():
    creds = None

    ''' The file token.pickle stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.'''

    if os.path.exists('token.pickle'):  # Check the existence of the file token.pickle.
        with open('token.pickle', 'rb') as token:  # If it does, open the file as rb (binary format for reading).
            creds = pickle.load(token)  # Assign the content of the token into creds.

    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:  # Check weather the creds is available, or it is valid.
        if creds and creds.expired and creds.refresh_token:  # If there's creds and creds is expired and there's \
            # a refresh token as well.
            creds.refresh(Request())  # Send a request for new token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
