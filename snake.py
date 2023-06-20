import pygame
from options import DIRECTION
from copy import deepcopy

class Snake:

    def __init__(self, pos_x, pos_y, cell_size, inner_color, outter_color, head_color):
        self.pos = [[pos_x, pos_y],
                        [pos_x, pos_y + cell_size],
                        [pos_x, pos_y + cell_size * 2],
                        ]
        self.cell_size = cell_size
        self.direction = DIRECTION.UP
        self.inner_color = inner_color
        self.outter_color = outter_color
        self.head_color = head_color


    def move(self):
        old_snake_pos = deepcopy(self.pos[:-1])
        if self.direction == DIRECTION.UP:
            self.pos[0][1] -= self.cell_size
        elif self.direction == DIRECTION.DOWN:
            self.pos[0][1] += self.cell_size
        elif self.direction == DIRECTION.LEFT:
            self.pos[0][0] -= self.cell_size
        elif self.direction == DIRECTION.RIGHT:
            self.pos[0][0] += self.cell_size

        self.pos = [self.pos[0]] + old_snake_pos
  
    def update(self):
        self.move()
    
    def draw(self, screen):
        head = True
        for body_part in self.pos:
            inner_rect = pygame.Rect((body_part[0], body_part[1], self.cell_size, self.cell_size))
            outter_rect = pygame.Rect((body_part[0] + 1, body_part[1] + 1, self.cell_size - 2, self.cell_size - 2))
            if not head:
                pygame.draw.rect(screen, self.inner_color, inner_rect)
            else:
                pygame.draw.rect(screen, self.head_color, inner_rect)
                head = False
            pygame.draw.rect(screen, self.outter_color, outter_rect, 2)