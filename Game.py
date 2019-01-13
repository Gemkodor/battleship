import sys
from random import randint

import pygame
from pygame.locals import *

from Board import Board
from IA import IA
from boats.Battleship import Battleship
from boats.Carrier import Carrier
from boats.Cruiser import Cruiser
from boats.Destroyer import Destroyer
from boats.Submarine import Submarine
from constants import *


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = None
        self.player_board = Board()
        self.enemy_board = Board()
        self.ia = IA()
        self.background = pygame.Surface(self.screen.get_size())

    @staticmethod
    def get_boats():
        return [Carrier(), Battleship(), Cruiser(), Submarine(), Destroyer()]

    def new_game(self):
        self.board = Board()
        self.place_player_boats()
        self.place_ia_boats()
        self.play()

    def place_player_boats(self):
        boats = Game.get_boats()

        for boat in boats:
            mouse_pos = pygame.mouse.get_pos()
            boat.pos = mouse_pos

            while not boat.is_placed:
                event = pygame.event.wait()
                if event.type == MOUSEMOTION:
                    boat.pos = event.pos
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == LEFT_CLICK:
                        self.player_board.place_player_boat(boat, event.pos)
                    elif event.button == RIGHT_CLICK:
                        boat.rotate()
                elif event.type == QUIT:
                    sys.exit()

                self.screen.blit(self.background, (0, 0))
                self.player_board.display(self.screen)
                boat.display(self.screen)
                pygame.display.flip()

    def place_ia_boats(self):
        boats = Game.get_boats()

        for boat in boats:
            while not boat.is_placed:
                pos = (randint(1, 10), randint(1, 10))
                orientation = randint(VERTICAL, HORIZONTAL)
                if boat.orientation != orientation:
                    boat.rotate()
                self.enemy_board.place_ia_boat(boat, pos)

                self.screen.blit(self.background, (0, 0))
                self.player_board.display(self.screen)
                boat.display(self.screen)
                pygame.display.flip()

    def play(self):
        self.enemy_board.display(self.screen, RIGHT)
        pygame.display.flip()
        end_game = False
        while not end_game:
            event = pygame.event.wait()

            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.enemy_board.is_valid_attack(event.pos):
                    successful_attack = self.enemy_board.player_attack(event.pos)
                    if self.enemy_board.nb_enemy_down == NB_ELEMENTS_TO_TAKE_DOWN:
                        end_game = True
                    elif not successful_attack:
                        end_game = self.ia.attack(self.player_board)

            self.screen.blit(self.background, (0, 0))
            self.player_board.display(self.screen, LEFT)
            self.enemy_board.display(self.screen, RIGHT)
            pygame.display.flip()

