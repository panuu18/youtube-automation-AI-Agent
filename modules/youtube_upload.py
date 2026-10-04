import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Authenticates the user and returns the YouTube API service."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secret.json'):
                raise FileNotFoundError(
                    "Missing 'client_secret.json'. You must download this from the Google Cloud Console "
                    "with the YouTube Data API enabled, and place it in the project root."
                )
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path: str, title: str, description: str, tags: list):
    """Uploads a video to YouTube."""
    youtube = get_authenticated_service()

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22' # 22 = People & Blogs
        },
        'status': {
            'privacyStatus': 'private', # Default to private for safety, change to 'public' when ready
            'selfDeclaredMadeForKids': False
        }
    }

    media_file = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    print(f"☁️ Uploading {video_path} to YouTube...")
    response = request.execute()
    
    video_id = response.get('id')
    print(f"✅ Video uploaded successfully! Video ID: {video_id}")
    return f"https://www.youtube.com/watch?v={video_id}"
