import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()


POST_URL = f'{os.getenv("MICROSERVICE_PATH")}/queue'
GET_URL = f'{os.getenv("MICROSERVICE_PATH")}/dequeue'
TOKEN = os.getenv('API_TOKEN')
message = {'link': 'https://www.youtube.com/watch?v=NTa6Xbzfq1U&ab_channel=ultragamemusic'}

# with requests.post(POST_URL, headers={'Authorization': '{key}'.format(key=TOKEN)}, json=message) as response:
#     print (response.text)# with requests.post(POST_URL, headers={'Authorization': '{key}'.format(key=TOKEN)}, json=message) as response:
#     print (response.text)

# check every 30 seconds if completed
start_time = time.perf_counter()
status_code = 0
while status_code != 200:
    # send get request
    with requests.get(GET_URL, headers={'Authorization': f'{TOKEN}'}) as response:
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

