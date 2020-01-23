from __future__ import print_function
import pickle
import os.path
import configparser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

config = configparser.ConfigParser()
config.read('structure_files/config.ini')
cred_path = config['googAPI']['cred_path']


# mod_path = "/".join(__file__.split("/")[:-2])
# with open('{}/config.ini'.format(mod_path)) as f:
#     cred_path = yaml.load(f, Loader=yaml.FullLoader)
#     cred_path = cred_path["cred_path"]

# Requested permissions from google user
SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/forms',
          'https://www.googleapis.com/auth/script.projects']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('{}/token.pickle'.format(cred_path)):
    with open('{}/token.pickle'.format(cred_path), 'rb') as token:
      creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '{}/credentials.json'.format(cred_path), SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('{}/token.pickle'.format(cred_path), 'wb') as token:
        pickle.dump(creds, token)


dv_service = build('drive', 'v3', credentials=creds)
st_service = build('sheets', 'v4', credentials=creds)
ml_service = build('gmail', 'v1', credentials=creds)
ap_service = build('script', 'v1', credentials=creds)




