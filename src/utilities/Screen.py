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
        pygame.time.Clock().tick(FrameConverter.FPS)

        # initialise screen populator
        self.__screen_populator = ScreenPopulator()

        # set gameboy image
        image = self.__screen_populator.get_gameboy_image()
        self.__screen = pygame.display.set_mode((image.get_width(), image.get_height()))
        pygame.display.set_caption("PlayBoy Visualiser")
        self.__screen.blit(image, (0, 0))

        # set up surface for red circles
        self.__screen.blit(self.__screen_populator.get_surface(), (0, 0))

        # render
        pygame.display.flip()

    def update(self, win_event=None):
        """
        Updates the screen in response to win_event (i.e renders red circles in response to input).
        If None, clears screen of red circles
        :param win_event: a pyboy Window Event
        """

        # update surface
        self.__screen_populator.update_screen(win_event)

        # add visual to screen
        self.__screen.blit(self.__screen_populator.get_surface(), (0, 0))

        # update display
        pygame.display.flip()


    def close_screen(self):
        pygame.quit()
        sys.exit()

