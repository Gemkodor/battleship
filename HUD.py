import pygame

from constants import *


class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)

    def draw(self, text, pos):
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, pos)
