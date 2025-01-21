import pygame as pg
import random as rd

pg.init()
width = 75
height = 75
size = 8
screen = pg.display.set_mode((width * size, height * size))
running = True
clock = pg.time.Clock()
dico = {
    "RW1": (7, 0),
    "KnW1": (7, 1),
    "BW1": (7, 2),
    "QW": (7, 3),
    "KW": (7, 4),
    "BW2": (7, 5),
    "KnW2": (7, 6),
    "RW2": (7, 7),
    "PW1": (6, 0),
    "PW2": (6, 1),
    "PW3": (6, 2),
    "PW4": (6, 3),
    "PW5": (6, 4),
    "PW6": (6, 5),
    "PW7": (6, 6),
    "PW8": (6, 7),
    "RB1": (0, 0),
    "KnB1": (0, 1),
    "BB1": (0, 2),
    "QB": (0, 3),
    "KB": (0, 4),
    "BB2": (0, 5),
    "KnB2": (0, 6),
    "RB2": (0, 7),
    "PB1": (1, 0),
    "PB2": (1, 1),
    "PB3": (1, 2),
    "PB4": (1, 3),
    "PB5": (1, 4),
    "PB6": (1, 5),
    "PB7": (1, 6),
    "PB8": (1, 7),
}
while running:
    clock.tick(10)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
            elif event.key == pg.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            elif event.key == pg.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pg.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pg.K_DOWN and direction != (0, -1):
                direction = (0, 1)
        elif event.type == pg.QUIT:
            running = False
    screen.fill((255, 255, 255))

    for i in range(size):
        for j in range(size):
            if (i + j) % 2 == 1:
                rect = pg.Rect(i * width, j * height, width, height)
                col = (91, 60, 17)
                pg.draw.rect(screen, col, rect)
            else:
                rect = pg.Rect(i * width, j * height, width, height)
                col = (169, 149, 123)
                pg.draw.rect(screen, col, rect)

    pg.display.update()
