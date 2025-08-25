import sys
import argparse
import pygame

from Grid import Grid
from GridCell import GridCell, CellState


def main():

    pygame.init()

    grid = init_grid()


    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Falling Sands")
    running = True
    mouse_down = False

    frame_counter = 0
    frames_per_update = max(1, int(TICKS_PER_SECOND/args.rainbow_speed))
    current_hue=0
    cell_color_at_current_time, current_hue = set_initial_color()

    while running:
        clock.tick(TICKS_PER_SECOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
        if mouse_down:
            frame_counter += 1
            current_hue = determine_color(cell_color_at_current_time, frame_counter, frames_per_update, current_hue)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x = mouse_x - MARGIN_X
            rel_y = mouse_y - MARGIN_Y
            for cell in grid.sprites:
                if cell.rect.collidepoint((rel_x, rel_y)):
                    (grid_x, grid_y) = cell.get_grid_position()
                    grid.cell_clicked(grid_x, grid_y, 10, 0.3)
        else:
            grid.set_cell_color(cell_color_at_current_time)


        draw_grid(grid.sprites, screen)
        simulation_step(grid)
        pygame.display.update()

    pygame.quit()
    sys.exit()


def init_grid():
    sprites = pygame.sprite.Group()
    grid_screen_width = SCREEN_WIDTH - MARGIN_X * 2 + BORDER_SIZE * 2
    grid_screen_height = SCREEN_HEIGHT - MARGIN_Y * 2 + BORDER_SIZE * 2

    grid_width = int(grid_screen_width / CELL_SIZE)
    grid_height = int(grid_screen_height / CELL_SIZE)

    grid = Grid(grid_width, grid_height, sprites)
    grid.configure_screenspace_vars(BORDER_SIZE, CELL_SIZE)

    for logical_y in range(grid_height):
        for logical_x in range(grid_width):
            grid.set_cell(logical_x, logical_y, args.no_borders)
    return grid

def draw_grid(grid_cells, screen):
    grid_width = SCREEN_WIDTH - MARGIN_X*2 + BORDER_SIZE*2
    grid_height = SCREEN_HEIGHT - MARGIN_Y*2 + BORDER_SIZE*2

    grid_surface = pygame.Surface((grid_width, grid_height))
    grid_surface.fill("#000000")
    pygame.draw.rect(grid_surface, pygame.Color('#ffffff'), (0,0, grid_width, grid_height), BORDER_SIZE)


    grid_cells.draw(grid_surface)
    screen.blit(grid_surface, (MARGIN_X,MARGIN_Y))

def simulation_step(grid):
    for y in range(grid.get_num_rows()):
        for x in range(grid.get_num_cols()):
            if grid.is_cell_filled(x, y):
                if y != 0:
                    if not grid.is_cell_filled(x, y - 1):
                        grid.set_cell_state(x, y, CellState.cell_falls_down)
                    elif not grid.is_cell_filled(x+1, y-1) and not grid.is_cell_filled(x-1, y-1):
                        grid.set_cell_state(x, y, CellState.cell_slides_left_or_right)
                    elif not grid.is_cell_filled(x+1, y-1):
                        grid.set_cell_state(x, y, CellState.cell_slides_right)
                    elif not grid.is_cell_filled(x-1, y-1):
                        grid.set_cell_state(x, y, CellState.cell_slides_left)
                    else:
                        grid.set_cell_state(x, y, CellState.cell_stable)

    grid.enact_cell_states()

def determine_color(cell_color_at_current_time, frame_counter, frames_per_update, current_hue):
    if args.rainbow:
        _, s, v, a = cell_color_at_current_time.hsva
        if frame_counter % frames_per_update == 0:
            current_hue += 0.5
        if current_hue > 360:
            current_hue = 0
        cell_color_at_current_time.hsva = (current_hue, s, v, a)
    return current_hue

def set_initial_color():
    if args.cell_color:
        try:
            color = pygame.Color(args.cell_color)
        except ValueError:
            raise Exception("Invalid cell color")
    else:
        if args.rainbow:
            color = pygame.Color('#ff0000')
        else:
            color = pygame.Color("#faf89d")
    current_hue = color.hsva[0]
    return color, current_hue


if __name__ == "__main__":
    print()
    print("=======================")
    print("FALLING SAND SIMULATION")
    print("=======================")
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cell-color", help="set cell color")
    parser.add_argument("-r", "--rainbow", help="rainbow sand", action="store_true")
    parser.add_argument("-rs", "--rainbow-speed", help="rainbow scroll rate, higher = faster (default 20)", type=float, default=20)
    parser.add_argument("-nb", "--no-borders", help="disable cell borders", action="store_true")
    args = parser.parse_args()
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    BORDER_SIZE = 1
    MARGIN_X = 100
    MARGIN_Y = 100
    CELL_SIZE = 5
    TICKS_PER_SECOND = 60
    main()