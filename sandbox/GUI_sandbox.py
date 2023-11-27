import os

import pygame
from src.utilities.Screen import Screen
from pyboy import WindowEvent
from dotenv import load_dotenv
from pyboy import PyBoy

load_dotenv()
screen = Screen()








event = WindowEvent.PRESS_ARROW_UP

i = 0

with PyBoy(os.getenv('GAME_PATH')) as pyboy:

    while not pyboy.tick():
        i += 1
        if (i % 60 == 0) and (event == WindowEvent.PRESS_ARROW_UP):
            event = WindowEvent.PRESS_ARROW_DOWN
            screen.update(win_event=event)

        elif i % 60 == 0:
            event = WindowEvent.PRESS_ARROW_UP
            screen.update(win_event=event)
        else:
            screen.update()




