import sys
import random
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 191, 0)
ROBIN_BLUE = (31, 206, 203)
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
        if keyboard[K_RIGHT] and self.snake.direction != 'left':
            self.snake.direction = 'right'
        elif keyboard[K_LEFT] and self.snake.direction != 'right':
            self.snake.direction = 'left'
        elif keyboard[K_UP] and self.snake.direction != 'down':
            self.snake.direction = 'up'
        elif keyboard[K_DOWN] and self.snake.direction != 'up':
            self.snake.direction = 'down'


grid = Grid(30)


def create_text(text, x, y, fontSize=20):
    mytext = pygame.font.Font("freesansbold.ttf", fontSize)
    textSurface = mytext.render(text, True, BLACK)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    SCREEN.blit(textSurface, textRect)


def create_button(msg, x, y, w, h, color, colorOnHover, action=None):
    myRect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(SCREEN, color, myRect)
    centerx, centery = myRect.center
    create_text(msg, centerx, centery, 30)
    mousex, mousey = pygame.mouse.get_pos()

    if x < mousex < x + w and y < mousey < y + h:
        pygame.draw.rect(SCREEN, colorOnHover, myRect)
        press = pygame.mouse.get_pressed()
        if press[0] == 1 and action != None:
            if msg == "Easy":
                FPS = 10
                action(FPS)
            elif msg == "Medium":
                FPS = 20
                action(FPS)
            else:
                FPS = 30
                action(FPS)


def check_quit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def difficulty():
    bg=pygame.transform.scale(pygame.image.load('bg.jfif'),(WIDTH,HEIGHT))
    while True:
        SCREEN.fill(WHITE)
        SCREEN.blit(bg,(0,0))
        create_button("Easy", WIDTH // 2 - 50, 100, 150, 50, GREEN, ROBIN_BLUE, main_game_loop)
        create_button("Medium", WIDTH // 2 - 50, 300, 150, 50, YELLOW, ROBIN_BLUE, main_game_loop)
        create_button("Hard", WIDTH // 2 - 50, 500, 150, 50, RED, ROBIN_BLUE, main_game_loop)
        pygame.display.update()
        check_quit()

        pygame.display.update()
        CLOCK.tick(30)


def main_game_loop(FPS):
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
        CLOCK.tick(FPS)


difficulty()
