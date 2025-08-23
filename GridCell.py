import pygame

class GridCell(pygame.sprite.Sprite):
    def __init__(self, x, y, size, filled=False):
        super().__init__()
        self.size = size
        self.filled = filled
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.position = (x,y)
        self.set_color()

    def set_color(self):
        if self.filled:
            color = "#555555"
        else:
            color = "#111111"
        self.image.fill(pygame.Color(color))

        pygame.draw.rect(
            self.image,  # surface to draw on
            pygame.Color("#333333"),  # border color
            self.image.get_rect(),  # rectangle covering the cell
            1  # thickness (1px)
        )

    def toggle_filled(self):
        if not self.filled:
            self.filled = True
            self.set_color()

