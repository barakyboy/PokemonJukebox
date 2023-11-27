import pygame
from dotenv import load_dotenv
import os
import sys

load_dotenv()
IMAGE_PATH = os.getenv('GAMEBOY_IMAGE_PATH')


# Initialize Pygame
pygame.init()

# Load an image
image = pygame.image.load(IMAGE_PATH)

screen = pygame.display.set_mode((image.get_width(), image.get_height()))
pygame.display.set_caption("Display Image")



# Set up the initial position for the image
image_pos = (0,0)
screen.blit(image, image_pos)
pygame.display.flip()
pygame.time.Clock().tick(30)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


