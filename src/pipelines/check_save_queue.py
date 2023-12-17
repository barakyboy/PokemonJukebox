# a pipeline for checking if a song is ready in microservice. If it is, queues it along with a thread denoting
# which song it is

# a pipeline to add a song to queue
from src.utilities.FrameConverter import FrameConverter
from queue import Queue
import threading
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import requests
import logging

load_dotenv()
PLAYABLE_DIR = os.getenv('PLAYABLE_DIR')
API_KEY = os.getenv('API_TOKEN')
API_ENDPOINT = os.getenv('API_ENDPOINT')


def check_save_queue(q: Queue):
    """
    adds a song to queue if one exists
    :param q: a queue of lists of framed notes and threads
    """

    # initialise
    audio_abs_path = ''
    message = ''
    try:

        # check if there is a song ready
        with requests.get(f'{API_ENDPOINT}/dequeue',
                          headers={'Authorization': '{key}'.format(key=API_KEY)}) as response:
            if response.status_code != 200:
                logging.debug(f"Could not dequeue; reason from response: {response.json()['message']}")
                return

            # if got to this point then got a proper response
            response_dict = response.json()

            # extract file_id for future reference
            file_id = response_dict.pop('file_id')

            logging.debug(f"Successfully pulled framed_notes data and file_id for file_id {file_id}")

            # convert response to framed notes
            fc = FrameConverter()
            framed_notes = fc.dict_to_frame(response_dict)


        # get file download
        message = {'file_id': file_id}
        with requests.post(f'{API_ENDPOINT}/download',
                          headers={'Authorization': '{key}'.format(key=API_KEY)}, json=message) as response:
            if response.status_code != 200:
                logging.debug(f"Could not download wav with file_id {file_id}\n"
                              f"reason from response: {response.json()['message']}")
                return

            logging.debug(f"Successfully downloaded file with file_id: {file_id}")
            # save file
            audio_abs_path = os.path.join(PLAYABLE_DIR, file_id) + '.wav'
            with open(audio_abs_path, 'wb') as file:
                file.write(response.content)


        # import wav audio
        audio = AudioSegment.from_file(audio_abs_path, format="wav")
        t = threading.Thread(target=play, args=(audio,))

        # add to queue
        q.put((framed_notes, t))

        logging.info(f"Successfully added file_id {file_id} to queue")

    except Exception as e:
        logging.exception(e)

    finally:

        if os.path.isfile(audio_abs_path):
            os.remove(audio_abs_path)

            # delete file on server side
            with requests.post(f'{API_ENDPOINT}/clean',
                               headers={'Authorization': '{key}'.format(key=API_KEY)}, json=message) as response:
                if response.status_code == 200:
                    logging.debug("Successfully deleted all files related to this song, both on server and client")

                else:
                    logging.debug("Successfully deleted all files related to this song, on client, but could not"
                                  "clean files on server. Reason:\n"
                                  f"{response.json()['message']}")





