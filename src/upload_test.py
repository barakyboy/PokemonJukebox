import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()

POST_URL = os.getenv('PYTHONANYWHERE_POST_URL')
GET_URL = os.getenv('PYTHONANYWHERE_GET_URL')
TOKEN = os.getenv('PYTHONANYWHERE_API_TOKEN')
MUS_PATH = os.path.join(os.getenv('OGG_DIR'), 'mus0.ogg')


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
        print('hello1')
        print(response.text)
        print('hello2')
        status_code = response.status_code
        time.sleep(30)


# End the timer
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Elapsed Time: {elapsed_time} seconds")

