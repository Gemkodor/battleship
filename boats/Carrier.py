import pygame

from boats.Boat import Boat


class Carrier(Boat):
    def __init__(self):
        super(Carrier, self).__init__()
        self.size = 5
        self.image = pygame.image.load("assets/carrier.png")
        self.image = pygame.transform.rotate(self.image, 90)
