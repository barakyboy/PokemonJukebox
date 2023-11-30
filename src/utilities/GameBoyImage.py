from dotenv import load_dotenv
import os
from pyboy import WindowEvent

load_dotenv()


class GameBoyImage:
    """
    A class that is responsible for knowing data about the gameboy image and encapsulating all data relating to the image
    itself, as well as converting window events to
    """
    IMAGE_PATH = os.getenv('GAMEBOY_IMAGE_PATH')

    # all are relative to top left being (0,0)
    EVENT_TO_CENTRE_MAP = {}
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_ARROW_UP] = (221, 262)
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_ARROW_DOWN] = (221, 310)
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_ARROW_RIGHT] = (246, 285)
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_ARROW_LEFT] = (197, 285)
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_BUTTON_A] = (375, 274)
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_BUTTON_B] = (337, 291)
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_BUTTON_SELECT] = (259, 341)
    EVENT_TO_CENTRE_MAP[WindowEvent.PRESS_BUTTON_START] = (298, 341)

    def convert_win_event_to_coordinates(self, win_event):
        """
        Takes a pyboy window event as input and returns the coordinate of the command it maps to.
        :param win_event: a pyboy window event
        :return: the coordinate of the control that the window event maps to.
        """
        return self.EVENT_TO_CENTRE_MAP[win_event]










