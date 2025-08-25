import pygame

from enum import Enum

class CellState(Enum):
    cell_stable = 1
    cell_falls_down = 2
    cell_slides_left = 3
    cell_slides_right = 4
    cell_slides_left_or_right = 6

class GridCell(pygame.sprite.Sprite):
    def __init__(self, x, y, grid_x, grid_y, size, sprite_group, filled=False):
        super().__init__()
        self.add(sprite_group)
        self.size = size
        self.filled = filled
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.screenPosition = (x,y)
        self.gridPosition = (grid_x, grid_y)
        self.draw(pygame.Color(0))
        self.state = CellState.cell_stable

    def draw(self, color_from_grid):
        if self.filled:
            color = color_from_grid
        else:
            color = pygame.Color(0)

        self.image.fill(color)

        pygame.draw.rect(
            self.image,  # surface to draw on
            pygame.Color("#333333"),  # border color
            self.image.get_rect(),  # rectangle covering the cell
            1  # thickness (1px)
        )

    def set_filled(self, is_filled, color_from_grid):
        self.filled = is_filled
        self.draw(color_from_grid)

    def is_filled(self):
        return self.filled

    def set_state(self, state:CellState):
        self.state = state

    def get_state(self):
        return self.state

    def get_grid_position(self):
        return self.gridPosition

