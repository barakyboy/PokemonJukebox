# service that monitors twitch and accepts requests for youtube links and sends them to AI_API

import socket
import dotenv
import os
import requests
import threading

dotenv.load_dotenv()
TWITCH_SERVER = os.getenv('TWITCH_SERVER')
TWITCH_PORT = os.getenv('TWITCH_PORT')
TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
TWITCH_NICKNAME = os.getenv('TWITCH_NICKNAME')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')
AI_API_TOKEN = os.getenv('AI_API_TOKEN')
AI_API_ENDPOINT = os.getenv('AI_API_ENDPOINT')


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




def main():
    # create and connect socket
    sock = socket.socket()
    sock.connect((TWITCH_SERVER, int(TWITCH_PORT)))
    sock.send(f"PASS {TWITCH_OAUTH_TOKEN}\n".encode('utf-8'))
    sock.send(f"NICK {TWITCH_NICKNAME}\n".encode('utf-8'))
    sock.send(f"JOIN {TWITCH_CHANNEL}\n".encode('utf-8'))
    sock.send("CAP REQ :twitch.tv/tags\n".encode('utf-8'))


    # create list to keep track of pipeline ids
    ids = []

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')
            resp_list = resp.split()

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            elif (resp_list[2] == 'PRIVMSG') and (isMod(resp_list[0])):
                # this is a message from mod, extract it
                mod_message = resp_list[4].strip(':')
                if mod_message.startswith('link: '):
                    link = mod_message.strip('link: ')

                    # send link to ai_api
                    message = {'link' : link}
                    with requests.post(f'{AI_API_ENDPOINT}/queue',
                                      headers={'Authorization': '{key}'.format(key=AI_API_TOKEN)}, json=message) as response:

                        # response the id for the pipeline
                        ids.append(response.json().get('id'))
                        print(f'appended pipeline with id: {ids[-1]}')

    except Exception as e:
        raise

    finally:
        # close socket
        sock.close()


if __name__ == '__main__':
    main()



