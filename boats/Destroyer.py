import pygame

from boats.Boat import Boat


class Destroyer(Boat):
    def __init__(self):
        super(Destroyer, self).__init__()
        self.size = 2
        self.image = pygame.image.load("assets/destroyer.png")
        self.image = pygame.transform.rotate(self.image, 90)
