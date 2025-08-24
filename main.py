import sys

import pygame
from typing import cast, List, Optional

from GridCell import GridCell


def main():

    pygame.init()

    grid_cells_sprites = pygame.sprite.Group()
    grid_matrix = init_grid(grid_cells_sprites)


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Falling Sands")
    running = True
    mouse_down = False
    last_cell = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rel_x = mouse_x - MARGIN_X
                rel_y = mouse_y - MARGIN_Y
                for cell in grid_cells_sprites:
                    if cell.rect.collidepoint((rel_x, rel_y)):
                        cell.toggle_filled()

                        last_cell = cell
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    rel_x = mouse_x - MARGIN_X
                    rel_y = mouse_y - MARGIN_Y
                    for cell in grid_cells_sprites:
                        if cell.rect.collidepoint((rel_x, rel_y)):
                            if cell != last_cell:
                                cell.toggle_filled()

                            last_cell = cell
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

        draw_grid(grid_cells_sprites, screen)
        simulation_step(grid_matrix)
        pygame.display.update()

    pygame.quit()
    sys.exit()


def init_grid(sprite_group):

    grid_width = SCREEN_WIDTH - MARGIN_X * 2 + BORDER_SIZE * 2
    grid_height = SCREEN_HEIGHT - MARGIN_Y * 2 + BORDER_SIZE * 2
    grid_x = 0
    grid_y = 0
    grid_matrix: List[List[Optional[GridCell]]] = [[None for _ in range(int(grid_width/CELL_SIZE)+1)] for _ in range(int(grid_height/CELL_SIZE)+1)]

    # Fix this loop
    for y in range(BORDER_SIZE, grid_width - BORDER_SIZE, CELL_SIZE):
        for x in range(BORDER_SIZE, grid_height - BORDER_SIZE, CELL_SIZE):
            cell = GridCell(x, y, grid_x, grid_y, CELL_SIZE, sprite_group, filled=False)
            print(grid_x, grid_y)
            grid_matrix[grid_x][grid_y] = cell
            grid_y+=1
        grid_x+=1
        grid_y=0

    return grid_matrix


def draw_grid(grid_cells, screen):
    grid_width = SCREEN_WIDTH - MARGIN_X*2 + BORDER_SIZE*2
    grid_height = SCREEN_HEIGHT - MARGIN_Y*2 + BORDER_SIZE*2

    grid_surface = pygame.Surface((grid_width, grid_height))
    grid_surface.fill("#000000")
    pygame.draw.rect(grid_surface, pygame.Color('#ffffff'), (0,0, grid_width, grid_height), BORDER_SIZE)


    grid_cells.draw(grid_surface)
    screen.blit(grid_surface, (MARGIN_X,MARGIN_Y))

def simulation_step(grid_matrix):
    for i in range(grid_matrix.shape[0]):
        for j in range(grid_matrix.shape[1]):
            if grid_matrix[i][j].filled:
                if j != 0 and not grid_matrix[i][j-1].filled:
                    grid_matrix[i][j-1].filled = True
                    grid_matrix[i][j].filled = False


if __name__ == "__main__":
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    BORDER_SIZE = 1
    MARGIN_X = 100
    MARGIN_Y = 100
    CELL_SIZE = 10
    main()