from pytube import YouTube
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate and create the PyDrive client.
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# Enter the YouTube URL
yt_url = 'YOUR_YOUTUBE_VIDEO_URL'
yt = YouTube(yt_url)

# List all available streams
streams = yt.streams.filter(file_extension='mp4')
for stream in streams:
    print(f'Res: {stream.resolution}, FPS: {stream.fps}, MIME: {stream.mime_type}')

# Set desired resolution
desired_resolution = '1080p'  # Change this to the resolution you want, e.g., '1080p', '480p', etc.

# Filter streams for the desired resolution
stream = yt.streams.filter(res=desired_resolution, file_extension='mp4').first()

if stream:
    # Download video to current directory
    stream.download()
    print(f'Download complete: {stream.default_filename}')

    # Upload the video to Google Drive
    upload_file = drive.CreateFile({'title': stream.default_filename})
    upload_file.SetContentFile(stream.default_filename)
    upload_file.Upload()
    print(f'Upload complete: {upload_file["title"]}')
    
    # Optionally, delete the downloaded video file from local
    os.remove(stream.default_filename)
else:
    print(f'No stream found with resolution {desired_resolution}')
