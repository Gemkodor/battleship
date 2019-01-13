import pygame

from boats.Boat import Boat


class Cruiser(Boat):
    def __init__(self):
        super(Cruiser, self).__init__()
        self.size = 3
        self.image = pygame.image.load("assets/cruiser.png")
        self.image = pygame.transform.rotate(self.image, 90)
