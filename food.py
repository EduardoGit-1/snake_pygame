import pygame

class Food:

    def __init__(self, pos_x, pos_y, cell_size, inner_color, outter_color):
        self.pos = [pos_x, pos_y]
        self.cell_size = cell_size
        self.inner_color = inner_color
        self.outter_color = outter_color
    
    def draw(self, screen):
        inner_rect = pygame.Rect((self.pos[0], self.pos[1], self.cell_size, self.cell_size))
        outter_rect = pygame.Rect((self.pos[0] + 1, self.pos[1] + 1, self.cell_size - 2, self.cell_size - 2))
        pygame.draw.rect(screen, self.inner_color, inner_rect)
        pygame.draw.rect(screen, self.outter_color, outter_rect, 2)
        