from random import randint

from constants import *


class IA:
    def __init__(self):
        self.before_last_success_pos = (0, 0)
        self.last_success_pos = (0, 0)

    @staticmethod
    def get_random_pos(board):
        valid_cell = False
        while not valid_cell:
            x, y = randint(1, 10), randint(1, 10)
            if board.content[x][y]["content"] == WATER or board.content[x][y]["content"] == PLAYER_BOAT:
                valid_cell = True

        return x, y

    def get_probable_orientation(self):
        if self.before_last_success_pos[0] == self.last_success_pos[0]:
            return HORIZONTAL
        elif self.before_last_success_pos[1] == self.last_success_pos[1]:
            return VERTICAL

    def get_best_move(self, board):
        x, y = self.last_success_pos
        if self.last_success_pos != (0, 0):
            probable_orientation = self.get_probable_orientation()
            if probable_orientation == HORIZONTAL:
                if x <= 9 and (board.content[x + 1][y]["content"] == WATER or
                               board.content[x + 1][y]["content"] == PLAYER_BOAT):
                    return x + 1, y
                if x >= 1 and (board.content[x - 1][y]["content"] == WATER or
                               board.content[x - 1][y]["content"] == PLAYER_BOAT):
                    return x - 1, y
                else:
                    self.before_last_success_pos = (0, 0)
                    self.last_success_pos = (0, 0)
                    return IA.get_random_pos(board)
            elif probable_orientation == VERTICAL:
                if y >= 1 and (board.content[x][y - 1]["content"] == WATER or
                               board.content[x][y - 1]["content"] == PLAYER_BOAT):
                    return x, y - 1
                if y <= 9 and (board.content[x][y + 1]["content"] == WATER or
                               board.content[x][y + 1]["content"] == PLAYER_BOAT):
                    return x, y + 1

        self.before_last_success_pos = (0, 0)
        self.last_success_pos = (0, 0)
        return IA.get_random_pos(board)

    def attack(self, board, explosion_sound):
        x, y = self.get_best_move(board)

        explosion_sound.play()
        if board.content[x][y]["content"] == PLAYER_BOAT:
            board.content[x][y]["content"] = WRECKAGE
            board.content[x][y]["surface"] = board.wreckage_img
            board.nb_player_down += 1
            self.before_last_success_pos = self.last_success_pos
            self.last_success_pos = (x, y)
            return True
        else:
            board.content[x][y]["content"] = WRECKAGE
            board.content[x][y]["surface"] = board.missed_target
            return False
