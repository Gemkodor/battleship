import pygame
import sys
from pygame.locals import *

from constants import *


class Label:
    def __init__(self, text, screen, style_on_hover, top, text_color=WHITE, pos=CENTER):
        self.font = pygame.font.Font(None, 50)
        self.padding_top = top
        self.text = text
        self.text_color = text_color
        self.pos = pos
        self.rect = None
        self.text_surface = None
        self.screen = screen
        self.style_on_hover = style_on_hover
        self.x_pos = 0
        self.render()

    def render(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        if self.pos == CENTER:
            self.x_pos = (self.screen.get_width() / 2) - (self.text_surface.get_width() / 2)
        self.rect = self.text_surface.get_rect()
        self.rect.topleft = (self.x_pos, self.padding_top)

    def draw(self, screen):
        self.render()
        screen.blit(self.text_surface, (self.x_pos, self.padding_top))

    def collides(self, pos):
        return self.rect.collidepoint(pos)

    def set_hovered_state(self, mouse_pos):
        if self.collides(mouse_pos) and self.style_on_hover:
            self.font.set_underline(True)
            self.font.set_bold(True)
        else:
            self.font.set_underline(False)
            self.font.set_bold(False)


class Menu:
    def __init__(self, screen):
        self.screen = screen

    def display(self):
        labels = {
            'title': Label("Bataille Navale", self.screen, False, top=10),
            'play': Label("Jouer", self.screen, True, top=250),
            'quit': Label("Quitter", self.screen, True, top=320)
        }

        choice = -1
        while choice == -1:
            event = pygame.event.wait()
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_j:
                    return LAUNCH_GAME
                if event.key == K_ESCAPE:
                    return QUIT_GAME
            if event.type == MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    if labels["play"].collides(event.pos):
                        return LAUNCH_GAME
                    elif labels["quit"].collides(event.pos):
                        sys.exit()

            self.screen.fill(BLACK)
            for key, label in labels.items():
                label.set_hovered_state(pygame.mouse.get_pos())
                label.draw(self.screen)

            pygame.display.flip()
