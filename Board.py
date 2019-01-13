import pygame

from constants import *


class Board:
    def __init__(self):
        self.content = list()
        self.surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.wreckage_img = pygame.image.load("assets/explosion.png")
        self.missed_target = pygame.image.load("assets/missed_target.png")
        self.create_board()
        self.x_pos = 0
        self.y_pos = 0
        self.nb_enemy_down = 0
        self.nb_player_down = 0

    def create_board(self):
        for i in range(BOARD_NB_COLS):
            row = list()
            for j in range(BOARD_NB_ROWS):
                box = pygame.Surface((BOARD_BOX_WIDTH, BOARD_BOX_HEIGHT))
                if i == 0 or j == 0:
                    box.fill(GRAY)
                else:
                    box.fill(BLUE)
                pygame.draw.rect(box, BLACK, box.get_rect(), 1)
                row.append({
                    'content': WATER,
                    'surface': box,
                    'boat': None,
                })
            self.content.append(row)

    def get_tile_coordinates(self, mouse_pos):
        # Get position relative to board
        x_pos = mouse_pos[0] - self.x_pos
        y_pos = mouse_pos[1] - self.y_pos

        # Get position in indexes
        x_tile = int(x_pos / BOARD_BOX_WIDTH)
        y_tile = int(y_pos / BOARD_BOX_HEIGHT)

        return x_tile, y_tile

    def display(self, container, position=LEFT):
        x_box = 0
        for row in self.content:
            y_box = 0
            for box in row:
                if box["boat"] is not None and box["content"] == PLAYER_BOAT:
                    if box["boat"].orientation == VERTICAL:
                        area = pygame.Rect(0, box["boat-zone"] * BOARD_BOX_HEIGHT, BOARD_BOX_WIDTH, BOARD_BOX_HEIGHT)
                    else:
                        area = pygame.Rect(box["boat-zone"] * BOARD_BOX_WIDTH, 0, BOARD_BOX_WIDTH, BOARD_BOX_HEIGHT)
                    self.surface.blit(box["boat"].image, (x_box, y_box), area)
                else:
                    self.surface.blit(box['surface'], (x_box, y_box))
                y_box += BOARD_BOX_HEIGHT
            x_box += BOARD_BOX_WIDTH

        if position == LEFT:
            self.x_pos = 50
            self.y_pos = 80
        elif position == RIGHT:
            self.x_pos = BOARD_WIDTH + 100
            self.y_pos = 80

        container.blit(self.surface, (self.x_pos, self.y_pos))

    def check_coordinates(self, boat, x_boat, y_boat):
        match_indexes = (1 <= x_boat <= 10 and 1 <= y_boat <= 10)
        fit_vertically = boat.orientation == VERTICAL and 1 <= y_boat <= 11 - boat.size
        fit_horizontally = boat.orientation == HORIZONTAL and 1 <= x_boat <= 11 - boat.size

        free_spot = True
        if match_indexes and (fit_vertically or fit_horizontally):
            for i in range(boat.size):
                if (boat.orientation == VERTICAL and self.content[x_boat][y_boat + i]["content"] != WATER) or \
                        (boat.orientation == HORIZONTAL and self.content[x_boat + i][y_boat]["content"] != WATER):
                    free_spot = False
                    break

        return match_indexes and (fit_vertically or fit_horizontally) and free_spot

    def place_ia_boat(self, boat, pos):
        x_boat, y_boat = pos[0], pos[1]

        if self.check_coordinates(boat, x_boat, y_boat):
            boat.pos = (x_boat, y_boat)
            boat.type = ENEMY_BOAT
            boat.color = GRAY
            self.place_boat(boat)

    def place_player_boat(self, boat, mouse_pos):
        x_boat, y_boat = self.get_tile_coordinates(mouse_pos)

        if self.check_coordinates(boat, x_boat, y_boat):
            boat.pos = (x_boat, y_boat)
            boat.type = PLAYER_BOAT
            boat.color = GREEN
            self.place_boat(boat)

    def place_boat(self, boat):
        x_pos, y_pos = boat.pos

        for i in range(boat.size):
            if boat.orientation == VERTICAL:
                self.content[x_pos][y_pos + i]["content"] = boat.type
                self.content[x_pos][y_pos + i]["boat"] = boat
                self.content[x_pos][y_pos + i]["boat-zone"] = i

            elif boat.orientation == HORIZONTAL:
                self.content[x_pos + i][y_pos]["content"] = boat.type
                self.content[x_pos + i][y_pos]["boat"] = boat
                self.content[x_pos + i][y_pos]["boat-zone"] = i

        boat.is_placed = True

    def is_valid_attack(self, mouse_pos):
        x, y = self.get_tile_coordinates(mouse_pos)

        match_indexes = (1 <= x <= 10 and 1 <= y <= 10)
        if match_indexes:
            content = self.content[x][y]["content"]
            return content == ENEMY_BOAT or content == WATER

        return False

    def player_attack(self, mouse_pos):
        x, y = self.get_tile_coordinates(mouse_pos)

        if self.content[x][y]["content"] == ENEMY_BOAT:
            self.content[x][y]["content"] = WRECKAGE
            self.content[x][y]["surface"] = self.wreckage_img
            self.nb_enemy_down += 1
            return True
        else:
            self.content[x][y]["content"] = WRECKAGE
            self.content[x][y]["surface"] = self.missed_target
            return False
