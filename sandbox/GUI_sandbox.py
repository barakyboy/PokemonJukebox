import pygame
from src.utilities.Screen import Screen
from pyboy import WindowEvent
from dotenv import load_dotenv

load_dotenv()
screen = Screen()








event = WindowEvent.PRESS_ARROW_UP

i = 0
RUNNING = True
while RUNNING:
    i += 2
    if (i % 60 == 0) and (event == WindowEvent.PRESS_ARROW_UP):
        event = WindowEvent.PRESS_ARROW_DOWN
    elif i % 60 == 0:
        event = WindowEvent.PRESS_ARROW_LEFT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

pygame.quit()

