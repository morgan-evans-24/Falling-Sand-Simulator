import sys

import pygame

def main():

    global SCREEN, MARGIN_X, MARGIN_Y, SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_SIZE

    pygame.init()
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    BORDER_SIZE = 1
    MARGIN_X = 100
    MARGIN_Y = 100

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Falling Sands")
    running = True

    while running:
        drawGrid();
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.quit()
    sys.exit()






def drawGrid():

    grid_width = SCREEN_WIDTH - MARGIN_X*2 + BORDER_SIZE*2
    grid_height = SCREEN_HEIGHT - MARGIN_Y*2 + BORDER_SIZE*2

    grid = pygame.Surface((grid_width, grid_height))
    grid_borders = pygame.Rect(0,0, grid_width, grid_height)
    grid.fill((0, 0, 0))
    pygame.draw.rect(grid, pygame.Color('#ffffff'), grid_borders, BORDER_SIZE)
    blockSize = 20;
    for x in range(BORDER_SIZE, grid_width - BORDER_SIZE, blockSize):
        for y in range(BORDER_SIZE, grid_height - BORDER_SIZE, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(grid, pygame.Color("#111111"), rect, 1)
    SCREEN.blit(grid, (MARGIN_X,MARGIN_Y))

if __name__ == "__main__":
    main()