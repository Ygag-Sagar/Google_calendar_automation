# from googleapiclient.discovery import build
# from oauth2client import file, client
#
# CREDENTIALS_FILE = './google-credentials.json'
#
# credentials = client.AccessTokenCredentials('ACCESS_TOKEN', 'USER_AGENT')
# service = build('calendar', 'v3', credentials=credentials)
# calendars = service.calendarList().list().execute()
# print(credentials)
import json
import base64

a = {
  "installed": {
    "client_id": "452887688695-fh24qormurv2g5jmmsqbr9fikkohadm0.apps.googleusercontent.com",
    "project_id": "test-for-youattendance",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": [
      "http://localhost"
    ]
  }
}
# convert json to a string
service_key = json.dumps(a)

# encode service key
encoded_service_key = base64.b64encode(service_key.encode('utf-8'))

print('ENCODED : ', encoded_service_key)

ENCODED :  b'eyJpbnN0YWxsZWQiOiB7ImNsaWVudF9pZCI6ICI0NTI4ODc2ODg2OTUtZmgyNHFvcm11cnYyZzVqbW1zcWJyOWZpa2tvaGFkbTAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCAicHJvamVjdF9pZCI6ICJ0ZXN0LWZvci15b3VhdHRlbmRhbmNlIiwgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwgImNsaWVudF9zZWNyZXQiOiAiR09DU1BYLVFNbm04LUh4YjcwTV9pTklSUGVYZFVvVFBtTG0iLCAicmVkaXJlY3RfdXJpcyI6IFsiaHR0cDovL2xvY2FsaG9zdCJdfX0='
