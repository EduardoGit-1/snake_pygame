import pygame
from options import *
from snake import Snake
from food import Food
from random import choice

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_font = pygame.font.SysFont(None, 40)
        self.subtitle_font = pygame.font.SysFont(None, 20)
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_food_needed = True
        self.game_over = False
        self.score = 0
        self.personal_best = 0
        self.board = pygame.Rect((0, CELL_SIZE * 5, SCREEN_WIDTH, SCREEN_HEIGHT - CELL_SIZE * 5))
        self.score_board = pygame.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - self.board.height))

        print(self.board.x, self.board.y)
        print("board width", self.board.w, "board height", self.board.h)

    
    def new_game(self):
        self.personal_best = self.score if self.score > self.personal_best else self.personal_best
        self.score = 0
        self.game_over = False
        self.snake = Snake(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), CELL_SIZE, SNAKE_INNER_COLOR, SNAKE_OUTTER_COLOR, SNAKE_HEAD_COLOR)
        self.food = Food(SCREEN_WIDTH + CELL_SIZE, SCREEN_HEIGHT + CELL_SIZE, CELL_SIZE, FOOD_INNER_COLOR, FOOD_OUTTER_COLOR)
        self.spawn_food()

    def update(self):
        self.snake.update()
        pygame.display.update()
        self.clock.tick(FPS)

    def draw(self):
        if self.game_over:
            self.draw_game_over()
        else:
            self.screen.fill("black")
            self.draw_board()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
        
    def draw_board(self):
        pygame.draw.rect(self.screen, "white", self.board, CELL_SIZE)
        pygame.draw.rect(self.screen, "blue", self.score_board, CELL_SIZE)
        score_render = self.title_font.render("SCORE: {}".format(self.score), True, "white")
        personal_best_render = self.title_font.render("BEST: {}".format(self.personal_best),True, "white")
        self.screen.blit(score_render, score_render.get_rect(center=(self.score_board.width // 4, self.score_board.height // 2)))
        self.screen.blit(personal_best_render, personal_best_render.get_rect(center=(self.score_board.width - self.score_board.width // 4, self.score_board.height // 2)))

    def draw_game_over(self):
        gameover_render = self.title_font.render(GAME_OVER_MESSAGE, True, "white")
        playagain_render = self.subtitle_font.render(PLAY_AGAIN_MESSAGE, True, "white")
        self.screen.blit(gameover_render, gameover_render.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
        self.screen.blit(playagain_render, playagain_render.get_rect(center=(SCREEN_WIDTH/2 , SCREEN_HEIGHT/2 + 25)))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.snake.direction != DIRECTION.RIGHT:
                    self.snake.direction = DIRECTION.LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != DIRECTION.LEFT:
                    self.snake.direction = DIRECTION.RIGHT
                elif event.key == pygame.K_UP and self.snake.direction != DIRECTION.DOWN:
                    self.snake.direction = DIRECTION.UP
                elif event.key == pygame.K_DOWN and self.snake.direction != DIRECTION.UP:
                    self.snake.direction = DIRECTION.DOWN
           
            if event.type == pygame.KEYDOWN and self.game_over:
                self.new_game()
    
    def run(self):
        self.new_game()
        while self.running:
            self.check_events()
            self.check_snake_body_collision()
            self.check_food_collision()
            self.check_screen_collision()
            self.update()
            self.draw()

        pygame.quit()
    
    def add_snake_segment(self):
        new_segment = self.snake.pos[-1]
        if self.snake.direction == DIRECTION.UP:
            new_segment[1] += CELL_SIZE
        if self.snake.direction == DIRECTION.DOWN:
            new_segment[1] -= CELL_SIZE
        if self.snake.direction == DIRECTION.RIGHT:
            new_segment[0] -= CELL_SIZE
        if self.snake.direction == DIRECTION.LEFT:
            new_segment[0] += CELL_SIZE

        self.snake.pos.append(new_segment)

    def check_food_collision(self):
         if self.snake.pos[0] == self.food.pos:
            self.spawn_food()
            self.add_snake_segment()
            self.increment_score()
    
    def check_screen_collision(self):
        #screen "x-axis collision"
        if self.snake.pos[0][0] == CELL_SIZE and self.snake.direction == DIRECTION.LEFT:
            self.snake.pos[0][0] = self.board.width - (CELL_SIZE * 2)
        elif self.snake.pos[0][0] > self.board.width - (CELL_SIZE * 3) and self.snake.direction == DIRECTION.RIGHT:
            self.snake.pos[0][0] = CELL_SIZE

        #screen "y-axis collision"
        if self.snake.pos[0][1] == self.board.height + self.board.y - (CELL_SIZE * 2 ) and self.snake.direction == DIRECTION.DOWN:
            self.snake.pos[0][1] = self.board.y + CELL_SIZE
        elif self.snake.pos[0][1] == self.board.y + CELL_SIZE and self.snake.direction == DIRECTION.UP:
            self.snake.pos[0][1] = self.board.height + self.board.y - (CELL_SIZE * 2 )       

    def check_snake_body_collision(self):
        snake_body = self.snake.pos[1:-1]
        if self.snake.pos[0] in snake_body:
            self.game_over = True
        
    def spawn_food(self):
        exclude_x_pos = set([item[0] for item in self.snake.pos])
        exclude_y_pos = set([item[1] for item in self.snake.pos])
        food_x_pos = int(choice(list(set([x for x in range(CELL_SIZE, int(SCREEN_WIDTH - CELL_SIZE), CELL_SIZE)]) - exclude_x_pos)))
        food_y_pos = int(choice(list(set([x for x in range(self.board.y + CELL_SIZE, int(SCREEN_HEIGHT-CELL_SIZE), CELL_SIZE)]) - exclude_y_pos)))
        self.food.pos = [food_x_pos, food_y_pos]

    def increment_score(self):
        self.score += 1

if __name__ == "__main__":
    game = Game()
    game.run()