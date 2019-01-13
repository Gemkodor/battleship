import pygame

from boats.Boat import Boat


class Battleship(Boat):
    def __init__(self):
        super(Battleship, self).__init__()
        self.size = 4
        self.image = pygame.image.load("assets/battleship.png")
        self.image = pygame.transform.rotate(self.image, 90)
