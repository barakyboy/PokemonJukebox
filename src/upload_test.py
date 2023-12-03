import requests
from dotenv import load_dotenv
import os
from utilities.MusicDownloader import MusicDownloader

load_dotenv()

POST_URL = f"https://{os.getenv('PYTHONANYWHERE_POST_URL')}"
TOKEN = os.getenv('PYTHONANYWHERE_API_TOKEN')
MUS_PATH = os.path.join(os.getenv('MP3_DIR'), 'mus0.mp3')

d = MusicDownloader()
d.download_youtube_link('https://www.youtube.com/watch?v=NTa6Xbzfq1U&ab_channel=ultragamemusic')

with open(MUS_PATH, 'rb') as file:

    files = {'file': file}

    with requests.post(POST_URL, headers={'Authorization': '{key}'.format(key=TOKEN)}, files=files) as response:

        print(response.text)

