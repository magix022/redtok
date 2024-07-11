import os
import pickle
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Function to authenticate and create the service
def authenticate():
    creds = None
    token_path = 'token.pickle'
    
    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token_file:
            info = pickle.load(token_file)
            creds = Credentials.from_authorized_user_info(json.loads(info))
            print(creds)


    # If there are no valid credentials available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds.to_json(), token)
    
    return build('drive', 'v3', credentials=creds)

# Function to upload file
def upload_file(service, file_path, folder_id=None):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id] if folder_id else []
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")


def create_folder(service, folder_name, parent_folder_id=None):
    try:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        file = service.files().create(body=file_metadata, fields='id').execute()
        print(f'Folder ID: {file.get("id")}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None
    return file

# Main function
if __name__ == '__main__':
    service = authenticate()
    folder_id = '1zYsZ6zorSRo0D_GxV0SIe5V5sKgd6kHD'  # Specify your folder ID
    file_path = 'example-videos/spanish.mp4'  # Specify the path to your video file
    #upload_file(service, file_path, folder_id)
    create_folder(service, 'test', folder_id)