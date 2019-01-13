import pygame

from boats.Boat import Boat


class Submarine(Boat):
    def __init__(self):
        super(Submarine, self).__init__()
        self.size = 3
        self.image = pygame.image.load("assets/submarine.png")
        self.image = pygame.transform.rotate(self.image, 90)
