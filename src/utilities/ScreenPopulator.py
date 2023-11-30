from src.utilities.GameBoyImage import GameBoyImage
import pygame


class ScreenPopulator:
    """
    A class that is responsible for populating screen elements
    """
    CIRCLE_RADIUS = 18
    CIRCLE_RGB = (241, 8, 60)
    CIRCLE_ALPHA = 169

    def __init__(self):
        # get gameboy image object
        self.__gameboy_image = GameBoyImage()
        self.__image_size = (self.get_gameboy_image().get_width(), self.get_gameboy_image().get_height())

        # create surface for creating semi-transparent objects
        self.__surface = pygame.Surface(self.__image_size, pygame.SRCALPHA)\

    def reset_surface(self):
        """
        Resets the surface of the ScreenPopulator, sl that there is nothing drawn on it
        """
        self.__surface.fill((0, 0, 0, 0))

    def get_surface(self):
        return self.__surface

    def get_gameboy_image(self):
        """
        Returns the gameboy pygame image object
        :return: the gameboy pygame image object
        """
        return pygame.image.load(self.__gameboy_image.IMAGE_PATH)

    def update_surface(self, win_event=None):
        """
        Takes a pyboy window event as input and renders a semi-transparent red circle at that input.
        If input is None, simply refreshes the surface (i.e removes all other input). If input is a
        window event that maps to something, refreshes surface and then renders on top of it
        :param win_event: a pyboy WindowEvent
        """
        self.reset_surface()
        if win_event is not None:
            pygame.draw.circle(self.__surface,
                               self.CIRCLE_RGB + (self.CIRCLE_ALPHA, ),
                               self.__gameboy_image.convert_win_event_to_coordinates(win_event),
                               self.CIRCLE_RADIUS)

