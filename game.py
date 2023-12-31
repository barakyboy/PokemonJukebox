from pyboy import PyBoy
from pyboy import WindowEvent
from dotenv import load_dotenv
import os
import time
from src.utilities.PitchControl import PitchControl
from src.utilities.Screen import Screen
from src.utilities.FrameConverter import FrameConverter
from queue import Queue
from src.utilities.Signal import Signal
from src.pipelines.check_save_queue import check_save_queue
import requests
import sys
import threading
import time
import logging


load_dotenv()
sys.path.append(os.getenv('PYTHONPATH'))
SLEEP_TIME = int(os.getenv('SLEEP_TIME'))
GAME_PATH = os.getenv('GAME_PATH')

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

def pipeline_manager(q: Queue):
    f"""
    A pipeline manager for the game. Checks for completed pipelines every {SLEEP_TIME} seconds
    :param q: the song queue
    """
    while True:
        try:
            # block for SLEEP_TIME
            logging.debug(f"pipeline manager sleeping for {SLEEP_TIME} seconds")
            time.sleep(SLEEP_TIME)

            # check for completed pipelines
            logging.debug(f"pipeline manager woke up! Checking for completed pipelines...")
            threading.Thread(target=check_save_queue, args=(q,)).start()

        except Exception as e:
            logging.exception(e)



def main():
    """
    :param q: a queue for managing the songs that are queued
    :param sig_q: a queue containing signals for inter thread communication
    """

    # initialise game queue
    q = Queue()

    # create pipeline manager thread
    threading.Thread(target=pipeline_manager, args=(q,)).start()

    # initialise controls dictionary
    release_dict = dict()
    release_dict[WindowEvent.PRESS_ARROW_UP] = WindowEvent.RELEASE_ARROW_UP
    release_dict[WindowEvent.PRESS_ARROW_DOWN] = WindowEvent.RELEASE_ARROW_DOWN
    release_dict[WindowEvent.PRESS_ARROW_LEFT] = WindowEvent.RELEASE_ARROW_LEFT
    release_dict[WindowEvent.PRESS_ARROW_RIGHT] = WindowEvent.RELEASE_ARROW_RIGHT
    release_dict[WindowEvent.PRESS_BUTTON_START] = WindowEvent.RELEASE_BUTTON_START
    release_dict[WindowEvent.PRESS_BUTTON_SELECT] = WindowEvent.RELEASE_BUTTON_SELECT
    release_dict[WindowEvent.PRESS_BUTTON_A] = WindowEvent.RELEASE_BUTTON_A
    release_dict[WindowEvent.PRESS_BUTTON_B] = WindowEvent.RELEASE_BUTTON_B

    # initial framed notes and curr states
    framed_notes = []
    curr = None

    # instantiate the gameboy screen visual
    screen = Screen()

    # instantiate game
    with PyBoy(GAME_PATH) as pyboy:

        pyboy.set_emulation_speed(target_speed=1)

        # initialise pitch controller
        pitch_controller = PitchControl()

        # game loop
        while not pyboy.tick():

            # check if no more instructions
            if curr is None:

                # get more instructions
                while q.empty():

                    # update visual
                    screen.update()

                    # give control back to player (for loading game, etc)
                    pyboy.tick()

                # queue is no longer empty, extract next song
                framed_notes, t = q.get()

                # get next note data
                curr = framed_notes.pop(0)

                # set frame to 0
                frame_num = 0

                # start song
                t.start()

            # check if there is an event on this frame
            if curr[0] == frame_num:

                # there is an event on this frame, execute it
                event = pitch_controller.get_control(curr[1])

                for i in range(FrameConverter.HOLD_FRAMES):
                    # hold for required number of frames
                    pyboy.send_input(event)

                    # update visual
                    screen.update(event)
                    # go to next frame
                    frame_num += 1
                    pyboy.tick()

                # release input
                pyboy.send_input(release_dict[event])

                # hold visual of last input for another frame
                screen.update(event)

                if len(framed_notes) == 0:
                    curr = None
                else:
                    curr = framed_notes.pop(0)

            else:
                screen.update()

            # increment frame num
            frame_num += 1


if __name__ == '__main__':
    main()

