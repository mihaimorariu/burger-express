import os
import pygame
from pygame.locals import *


def LoadImage(subfolder, file_name, colorkey):
    full_name = os.path.join(subfolder, file_name)

    image = pygame.image.load(full_name)
    image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()
