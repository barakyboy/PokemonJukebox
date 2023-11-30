import pygame
from src.utilities.ScreenPopulator import ScreenPopulator
from src.utilities.FrameConverter import FrameConverter
import sys


class Screen:
    """
    A class responsible for displaying visual represention of gameboy screen as well as its inputs
    """

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # initialise screen populator
        self.__screen_populator = ScreenPopulator()

        # set gameboy image
        self.__image = self.__screen_populator.get_gameboy_image()
        self.__screen = pygame.display.set_mode((self.__image.get_width(), self.__image.get_height()))
        pygame.display.set_caption("GameBoy Visualiser")

    def update(self, win_event=None):
        """
        Updates the screen in response to win_event (i.e renders red circles in response to input).
        If None, clears screen of red circles
        :param win_event: a pyboy Window Event
        """

        # refresh gameboy image
        self.__screen.blit(self.__image, (0, 0))

        # update surface
        self.__screen_populator.update_surface(win_event)

        # add visual to screen
        self.__screen.blit(self.__screen_populator.get_surface(), (0, 0))

        # update display
        pygame.display.flip()


    def close_screen(self):
        pygame.quit()
        sys.exit()

