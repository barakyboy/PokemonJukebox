# service that monitors twitch and accepts requests for youtube links and sends them to AI_API

import socket
import dotenv
import os
import requests
import threading
import time
import logging

dotenv.load_dotenv()
TWITCH_SERVER = os.getenv('TWITCH_SERVER')
TWITCH_PORT = os.getenv('TWITCH_PORT')
TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
TWITCH_NICKNAME = os.getenv('TWITCH_NICKNAME')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')
AI_API_TOKEN = os.getenv('AI_API_TOKEN')
AI_API_ENDPOINT = os.getenv('AI_API_ENDPOINT')
CHECK_FREQ = int(os.getenv('CHECK_FREQ'))


def isMod(badge: str):
    """
    Returns true if the badge comes from a moderator
    :param badge: a badge returned by IRC
    :return: a boolean value denoting whether the user is a moderator
    """
    badge_list = badge.split(';')
    for badge in badge_list:
        if badge.startswith('mod='):
            # check whether mod
            return bool(int(badge.split('mod=')[1]))

    return False

def isBroadcaster(badge: str):
    """
    Returns true if the badge comes from a moderator or broadcaster
    :param badge: a badge returned by IRC
    :return: a boolean value denoting whether the user is a broadcaster
    """
    badge_list = badge.split(';')
    for badge in badge_list:
        if badge.startswith('badges='):
            # check whether broadcaster
            return badge[len('badges='):] == 'broadcaster/1'

    return False


def status_loop(pipeline_list: list):
    f"""
    queries the ai_api every {CHECK_FREQ} seconds to check on status of running pipelines. Then sends this data
    to the front end.
    : param pipeline_list: a list of pipeline uuids
    """

    # mutex for iterating over list
    mutex = threading.Lock()

    while True:

        # block thread for an amount of time
        logging.debug(f'status loop sleeping for {CHECK_FREQ} seconds...')
        time.sleep(CHECK_FREQ)
        logging.debug(f'status loop woke up!')


        # check on status
        message = {'pipeline_uuids': pipeline_list}
        with mutex:
            with requests.post(f'{AI_API_ENDPOINT}/status',
                               headers={'Authorization': '{key}'.format(key=AI_API_TOKEN)}, json=message) as response:

                if response.status_code == 200:
                    response_dict = response.json()
                    to_delete = []
                    for pipeline_uuid in response_dict.keys():
                        ## TO DO: CODE TO CREATE RESPONSE FOR FRONT END HERE
                        logging.info(f'pipeline status: {pipeline_uuid} : {response_dict[pipeline_uuid]}')
                        if (response_dict[pipeline_uuid] == 1) or (response_dict[pipeline_uuid] == 3):
                            # failed or completed
                            to_delete.append(pipeline_uuid)

                    # send to front end


                    # delete failed or completed from pipeline list
                    for pipeline_uuid in to_delete:
                        pipeline_list.remove(pipeline_uuid)

                else:
                    logging.error(response.text)


def main():

    # initialise logger
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    # create list to keep track of pipelines
    pipelines = list()

    # create mutex for multithreading
    mutex = threading.Lock()

    # start status_loop
    threading.Thread(target=status_loop, args=(pipelines,)).start()


    # create and connect socket
    sock = socket.socket()
    sock.connect((TWITCH_SERVER, int(TWITCH_PORT)))
    sock.send(f"PASS {TWITCH_OAUTH_TOKEN}\n".encode('utf-8'))
    sock.send(f"NICK {TWITCH_NICKNAME}\n".encode('utf-8'))
    sock.send(f"JOIN {TWITCH_CHANNEL}\n".encode('utf-8'))
    sock.send("CAP REQ :twitch.tv/tags\n".encode('utf-8'))
    logging.debug("socket connection established")

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')
            logging.info(f'socket response: {resp}')
            resp_list = resp.split()

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            elif (resp_list[2] == 'PRIVMSG') and (isMod(resp_list[0]) or isBroadcaster(resp_list[0])):
                logging.debug("Last received message is from mod or broadcaster")
                # this is a message from mod or broadcaster, extract it
                # remove starting semicolon
                mod_message = resp_list[4][1:]
                if mod_message.startswith('link:'):
                    link = mod_message[len('link:'):]

                    # send link to ai_api
                    message = {'link': link}
                    with requests.post(f'{AI_API_ENDPOINT}/queue',
                                      headers={'Authorization': '{key}'.format(key=AI_API_TOKEN)}, json=message) as response:

                        # add id to list
                        with mutex:
                            response_uuid = response.json().get('id')
                            pipelines.append(response_uuid)
                            logging.info(f"appended pipeline with id: {response_uuid}")

    except Exception as e:
        raise

    finally:
        # close socket
        sock.close()


if __name__ == '__main__':
    main()



