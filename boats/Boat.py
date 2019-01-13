import pygame

from constants import *


class Boat(pygame.sprite.Sprite):
    def __init__(self):
        self.pos = (0, 0)
        self.is_placed = False
        self.orientation = VERTICAL
        self.image = None

    def rotate(self):
        if self.orientation == VERTICAL:
            self.image = pygame.transform.rotate(self.image, 90)
            self.orientation = HORIZONTAL
        else:
            self.image = pygame.transform.rotate(self.image, -90)
            self.orientation = VERTICAL

    def display(self, container):
        x, y = self.pos

        if self.orientation == VERTICAL:
            container.blit(self.image, (x - (self.image.get_width() / 2), y - 10))
        else:
            container.blit(self.image, (x - 10, y - (self.image.get_height() / 2)))
