import pygame

from Game import Game
from Menu import Menu
from constants import *

pygame.init()
pygame.display.set_caption("Bataille navale")

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
menu = Menu(screen)

running = True
while running:
    choice = menu.display()
    if choice == QUIT_GAME:
        running = False
    elif choice == LAUNCH_GAME:
        game = Game(screen)
        game.new_game()
