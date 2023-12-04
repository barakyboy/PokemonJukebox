import requests
from dotenv import load_dotenv
import os
from utilities.MusicDownloader import MusicDownloader
import time

load_dotenv()

POST_URL = f"https://{os.getenv('PYTHONANYWHERE_POST_URL')}"
GET_URL = f"https://{os.getenv('PYTHONANYWHERE_GET_URL')}"
TOKEN = os.getenv('PYTHONANYWHERE_API_TOKEN')
MUS_PATH = os.path.join(os.getenv('MP3_DIR'), 'mus0.mp3')

d = MusicDownloader()
d.download_youtube_link('https://www.youtube.com/watch?v=NTa6Xbzfq1U&ab_channel=ultragamemusic')

with open(MUS_PATH, 'rb') as file:

    files = {'file': file}

    with requests.post(POST_URL, headers={'Authorization': '{key}'.format(key=TOKEN)}, files=files) as response:

        print(response.text)

# check every 30 seconds if completed
start_time = time.perf_counter()
status_code = 0
while status_code != 200:
    # send get request
    with requests.get(GET_URL, headers={'Authorization': '{key}'.format(key=TOKEN)}) as response:
        print(response.text)
        status_code = response.status_code

# End the timer
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Elapsed Time: {elapsed_time} seconds")

