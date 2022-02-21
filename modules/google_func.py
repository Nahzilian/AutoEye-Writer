import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from .secrets import SCOPES, FOLDER_ID

def get_google_cred() -> Credentials:
    """
    Generate token for Google API
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    creds: Credentials = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_files_id(creds: Credentials) -> list:
    files = []
    folder_id = FOLDER_ID
    try:
        service = build('drive', 'v3', credentials=creds)

        query = f"parents = '{folder_id}'"
        # Retrieve the documents contents from the Docs service.
        res = service.files().list(q=query).execute()
        f = res.get('files')
        for file in f:
            files.append(file.get('id'))
        # nextPage = res.get('nextPageToken')

        # print(res)
        # while nextPage :
        #     res = service.files().list(q=query).execute()
        #     files.extend(res.get('files'))
        #     nextPage = res.get('nextPageToken')
    except HttpError as err:
        print(err)
    return files


def get_file_by_id(id: str, creds: Credentials) -> dict:
    try:
        service = build('docs', 'v1', credentials=creds)
        document = service.documents().get(documentId=id).execute()
        if not document.get('body'):
            raise TypeError
        return document
    except HttpError as err:
        print(err)
    return {}


    