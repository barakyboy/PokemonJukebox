import socket
import dotenv
import os


dotenv.load_dotenv()
TWITCH_SERVER = os.getenv('TWITCH_SERVER')
TWITCH_PORT = os.getenv('TWITCH_PORT')
TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
TWITCH_NICKNAME = os.getenv('TWITCH_NICKNAME')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')


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




# create and connect socket
sock = socket.socket()
sock.connect((TWITCH_SERVER, int(TWITCH_PORT)))
sock.send(f"PASS {TWITCH_OAUTH_TOKEN}\n".encode('utf-8'))
sock.send(f"NICK {TWITCH_NICKNAME}\n".encode('utf-8'))
sock.send(f"JOIN {TWITCH_CHANNEL}\n".encode('utf-8'))
sock.send("CAP REQ :twitch.tv/tags\n".encode('utf-8'))

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
            ### WRITE CODE TO DO THIS HERE






# close socket
sock.close()



