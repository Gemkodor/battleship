import sys
import time
from random import randint

import pygame
from pygame.locals import *

from Board import Board
from HUD import HUD
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
        self.hud = HUD(screen)
        self.player_board = Board()
        self.enemy_board = Board()
        self.ia = IA()
        self.background = pygame.Surface(self.screen.get_size())
        self.player_round = True
        self.explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

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
                self.hud.draw("Placez vos bateaux", (700, 200))
                self.hud.draw("Clic-droit pour changer de sens", (700, 250))
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
            elif self.player_round and event.type == MOUSEBUTTONDOWN and self.enemy_board.is_valid_attack(event.pos):
                self.explosion_sound.play()
                successful_attack = self.enemy_board.player_attack(event.pos)
                self.update_game_screen()
                if not successful_attack:
                    self.player_round = False
                if self.enemy_board.nb_enemy_down == NB_ELEMENTS_TO_TAKE_DOWN:
                    self.show_end_game_screen(HUMAN_PLAYER)
                    end_game = True

            if not self.player_round:
                self.update_game_screen()
                time.sleep(1)
                while self.ia.attack(self.player_board, self.explosion_sound):
                    self.update_game_screen()
                    time.sleep(1)
                self.player_round = True
                if self.player_board.nb_player_down == NB_ELEMENTS_TO_TAKE_DOWN:
                    self.show_end_game_screen(IA_PLAYER)
                    end_game = True

            if pygame.event.peek(MOUSEBUTTONDOWN):
                pygame.event.clear(MOUSEBUTTONDOWN)

            if not end_game:
                self.update_game_screen()

    def update_game_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.player_board.display(self.screen, LEFT)
        self.enemy_board.display(self.screen, RIGHT)
        if self.player_round:
            self.hud.draw("A vous de jouer !", (510, 700))
        else:
            self.hud.draw("L'ordinateur est en train de jouer !", (400, 700))
        pygame.display.flip()

    def show_end_game_screen(self, winner):
        return_to_menu = False
        while not return_to_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    return_to_menu = True

                self.screen.blit(self.background, (0, 0))
                if winner == HUMAN_PLAYER:
                    self.hud.draw("Bravo ! Vous avez gagné !", (450, 350))
                else:
                    self.hud.draw("Perdu ! L'ordinateur vous a battu !", (400, 350))

                self.hud.draw("Appuyez sur une touche pour revenir au menu", (300, 700))
                pygame.display.flip()
