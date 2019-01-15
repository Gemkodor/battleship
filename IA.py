from random import randint

from constants import *


class IA:
    def __init__(self):
        self.before_last_success_pos = (-1, -1)
        self.last_success_pos = (-1, -1)
        self.last_attack_successful = False

    @staticmethod
    def get_random_pos(board):
        valid_cell = False
        while not valid_cell:
            x, y = randint(1, 10), randint(1, 10)
            if board.content[x][y]["content"] == WATER or board.content[x][y]["content"] == PLAYER_BOAT:
                valid_cell = True

        return x, y

    def get_probable_orientation(self):
        if self.before_last_success_pos != (-1, -1) and self.last_success_pos != (-1, -1):
            if self.before_last_success_pos[0] == self.last_success_pos[0]:
                return VERTICAL
            if self.before_last_success_pos[1] == self.last_success_pos[1]:
                return HORIZONTAL

        return randint(VERTICAL, HORIZONTAL)

    def get_best_move(self, board):
        x, y = self.last_success_pos
        if self.last_success_pos != (-1, -1):
            probable_orientation = self.get_probable_orientation()

            if probable_orientation == HORIZONTAL:
                if x <= 9 and (board.content[x + 1][y]["content"] == WATER or
                               board.content[x + 1][y]["content"] == PLAYER_BOAT):
                    return x + 1, y
                elif x >= 1 and (board.content[x - 1][y]["content"] == WATER or
                                 board.content[x - 1][y]["content"] == PLAYER_BOAT):
                    return x - 1, y
                elif self.before_last_attack_successful:
                    i = 1
                    while x + i <= 9 and x - i >= 1:
                        if board.content[x + i][y]["content"] == WATER or board.content[x + i][y]["content"] == PLAYER_BOAT:
                            return x + i, y
                        if board.content[x - i][y]["content"] == WATER or board.content[x - i][y]["content"] == PLAYER_BOAT:
                            return x - i, y
                        i += 1
            elif probable_orientation == VERTICAL:
                if y >= 1 and (board.content[x][y - 1]["content"] == WATER or
                               board.content[x][y - 1]["content"] == PLAYER_BOAT):
                    return x, y - 1
                elif y <= 9 and (board.content[x][y + 1]["content"] == WATER or
                                 board.content[x][y + 1]["content"] == PLAYER_BOAT):
                    return x, y + 1
                elif self.before_last_attack_successful:
                    i = 1
                    while y + i <= 9 and y - i >= 1:
                        if board.content[x][y + i]["content"] == WATER or board.content[x][y + i]["content"] == PLAYER_BOAT:
                            return x, y + i
                        if board.content[x][y - i]["content"] == WATER or board.content[x][y - i]["content"] == PLAYER_BOAT:
                            return x, y - i
                        i += 1

        return IA.get_random_pos(board)

    def attack(self, board, explosion_sound):
        x, y = self.get_best_move(board)

        explosion_sound.play()
        if board.content[x][y]["content"] == PLAYER_BOAT:
            board.content[x][y]["content"] = WRECKAGE
            board.content[x][y]["surface"] = board.wreckage_img
            board.nb_player_down += 1

            if self.last_success_pos != (-1, -1):
                self.before_last_success_pos = self.last_success_pos
                self.before_last_attack_successful = True
            self.last_success_pos = (x, y)

            self.last_attack_successful = True

            return True
        else:
            board.content[x][y]["content"] = WRECKAGE
            board.content[x][y]["surface"] = board.missed_target

            if not self.last_attack_successful:
                self.before_last_attack_successful = False
            self.last_attack_successful = False

            return False
