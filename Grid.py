import random
from typing import List, Optional

import pygame

from GridCell import GridCell, CellState


class Grid:
    def __init__(self, num_cols, num_rows, sprites):
        self.sprites = sprites
        self.height = num_rows
        self.width = num_cols
        self.grid: List[List[Optional[GridCell]]] = [[None for _ in range(num_cols)] for _ in range(num_rows)]
        self.cell_color = pygame.Color(0)
        self.BORDER_SIZE = 1
        self.CELL_SIZE = 10

    def configure_screenspace_vars(self, BORDER_SIZE, CELL_SIZE):
        self.BORDER_SIZE = BORDER_SIZE
        self.CELL_SIZE = CELL_SIZE

    def set_cell_color(self, cell_color):
        self.cell_color = cell_color

    def set_cell(self, x, y, borders):
        screen_x, screen_y = self._calc_screen_coords(x, y, self.height)
        cell = GridCell(screen_x, screen_y, x, y, self.CELL_SIZE, sprite_group=self.sprites, filled=False, no_borders=borders)
        self.grid[y][x] = cell

    def _get_cell(self, x, y):
        return self.grid[y][x]

    def cell_clicked(self, x, y, brush_radius, brush_saturation):
        cell = self._get_cell(x, y)
        if not cell.is_filled():
            cell.set_filled(True, self.cell_color)
        for local_y in range(y-brush_radius, y+brush_radius, 1):
            for local_x in range(x-brush_radius, x+brush_radius, 1):
                if local_x < 0 or local_x >= self.width or local_y < 0 or local_y >= self.height:
                    continue
                if random.random() < brush_saturation and not self._get_cell(local_x, local_y).is_filled():
                    self._get_cell(local_x, local_y).set_filled(True, self.cell_color)

    def is_cell_filled(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        else:
            return self.grid[y][x].filled

    def set_cell_state(self, x, y, state: CellState):
        self.grid[y][x].set_state(state)

    def _get_cell_state(self, x, y):
        return self.grid[y][x].state

    def _enact_cell_state(self, x, y):
        match self._get_cell_state(x, y):
            case CellState.cell_falls_down:
                self._get_cell(x, y-1).set_filled(True, self.cell_color)
                self._get_cell(x, y).set_filled(False, self.cell_color)
            case CellState.cell_slides_left:
                self._get_cell(x - 1, y - 1).set_filled(True, self.cell_color)
                self._get_cell(x, y).set_filled(False, self.cell_color)
            case CellState.cell_slides_right:
                self._get_cell(x + 1, y - 1).set_filled(True, self.cell_color)
                self._get_cell(x, y).set_filled(False, self.cell_color)
            case CellState.cell_slides_left_or_right:
                if random.random() < 0.5:
                    self._get_cell(x - 1, y - 1).set_filled(True, self.cell_color)
                else:
                    self._get_cell(x + 1, y - 1).set_filled(False, self.cell_color)
                self._get_cell(x, y).set_filled(False, self.cell_color)
        self.set_cell_state(x, y, CellState.cell_stable)

    def enact_cell_states(self):
        # It's bad practice to shadow variable names from outer scope.
        for local_y in range(0, self.height):
            for local_x in range(0, self.width):
                self._enact_cell_state(local_x, local_y)




    def get_num_cols(self):
        return self.width

    def get_num_rows(self):
        return self.height

    def get_sprites(self):
        return self.sprites

    def _calc_screen_coords(self, logical_x, logical_y, grid_height):
        screen_x = self.BORDER_SIZE + logical_x * self.CELL_SIZE
        screen_y = self.BORDER_SIZE + (grid_height - logical_y - 1) * self.CELL_SIZE
        return screen_x, screen_y