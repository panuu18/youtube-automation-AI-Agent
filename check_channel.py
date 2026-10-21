import pickle
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def check_channel():
    if not os.path.exists('token.pickle'):
        print("No token.pickle found!")
        return

    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        
    youtube = build('youtube', 'v3', credentials=creds)
    
    request = youtube.channels().list(
        part="snippet",
        mine=True
    )
    response = request.execute()
    
    if 'items' in response:
        for channel in response['items']:
            print(f"✅ Bot is connected to channel: {channel['snippet']['title']}")
            print(f"Channel ID: {channel['id']}")
    else:
        print("❌ Connected to a Google Account, but it doesn't have a YouTube channel!")

if __name__ == "__main__":
    check_channel()
