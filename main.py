import sys
import random
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
WIDTH = 600
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.init()


class Snake:
    def __init__(self):
        self.length = 1
        self.body = [[0, 0]]
        self.color = WHITE
        self.direction = None

        pass

    def move(self):
        if self.direction == 'right':
            self.body.append([self.body[-1][0], self.body[-1][1] + 1])
            self.body.pop(0)
        elif self.direction == 'left':
            self.body.append([self.body[-1][0], self.body[-1][1] - 1])
            self.body.pop(0)
        elif self.direction == 'up':
            self.body.append([self.body[-1][0] - 1, self.body[-1][1]])
            self.body.pop(0)
        elif self.direction == 'down':
            self.body.append([self.body[-1][0] + 1, self.body[-1][1]])
            self.body.pop(0)

    def add_length(self, row, col):
        self.length += 1
        if self.direction == 'right':
            self.body.append([row, col + 1])
        if self.direction == 'left':
            self.body.append([row, col - 1])
        if self.direction == 'up':
            self.body.append([row - 1, col])
        if self.direction == 'down':
            self.body.append([row + 1, col])


class Grid:
    def __init__(self, size):
        self.snake = Snake()
        self.size = size
        self.grid = [[None for i in range(size)] for j in range(size)]
        self.food = [random.randint(1, size - 1), random.randint(1, size - 1)]
        for i in range(0, size):
            for j in range(0, size):
                self.grid[j][i] = pygame.Rect(i * (WIDTH // size), j * (HEIGHT // size), WIDTH // size, HEIGHT // size)

    def draw_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.rect(SCREEN, WHITE, self.grid[i][j], 1)
        pass

    def draw_snake(self):
        for row, col in self.snake.body:
            if 0 <= row <= self.size - 1 and 0 <= col <= self.size - 1:
                pygame.draw.rect(SCREEN, self.snake.color, self.grid[row][col])
            else:
                pygame.quit()
                sys.exit()

    def check_self_collapse(self):
        if self.snake.body[-1] in self.snake.body[:-1]:
            pygame.quit()
            sys.exit()

    def generate_food(self):
        if self.snake.body[-1] == self.food:
            self.food = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
            self.snake.add_length(self.snake.body[-1][0], self.snake.body[-1][1])
        pygame.draw.rect(SCREEN, RED, self.grid[self.food[0]][self.food[1]])

    def check_keyboard(self):
        keyboard = pygame.key.get_pressed()
        if keyboard[K_RIGHT] and self.snake.direction!='left':
            self.snake.direction = 'right'
        elif keyboard[K_LEFT] and self.snake.direction!='right':
            self.snake.direction = 'left'
        elif keyboard[K_UP] and self.snake.direction!='down':
            self.snake.direction = 'up'
        elif keyboard[K_DOWN] and self.snake.direction!='up':
            self.snake.direction = 'down'


grid = Grid(30)


def check_quit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def main_game_loop():
    game = True
    while game:
        SCREEN.fill(BLACK)
        check_quit()
        grid.snake.move()
        grid.check_keyboard()
        grid.draw_grid()
        grid.check_self_collapse()
        grid.draw_snake()
        grid.generate_food()
        pygame.display.update()
        CLOCK.tick(15)


main_game_loop()
