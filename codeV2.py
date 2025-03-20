import pygame as pg
import random as rd
import numpy as np

pg.init()
width = 80
height = 80
size = 8
ecran = pg.display.set_mode((width * size, height * size))
running = True
clock = pg.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
screen = [[None for i in range(8)] for j in range(8)]


class Piece:
    def __init__(self, color, n, m):
        self.color = color
        self.x = n * width
        self.y = m * height


class Pawn(Piece):
    def coup_valide(self, start, end, screen):
        if self.color == "black":
            if (
                start[0] == end[0]
                and start[1] + 1 == end[1]
                and screen[end[0]][end[1]] is None
            ):
                return True
            elif (
                start[0] == end[0]
                and start[1] + 2 == end[1]
                and start[1] == 1
                and screen[end[0]][end[1]] is None
            ):
                return True
            elif (
                start[0] + 1 == end[0]
                and start[1] + 1 == end[1]
                and screen[end[0]][end[1]] is not None
            ):
                return True
            elif (
                start[0] - 1 == end[0]
                and start[1] + 1 == end[1]
                and screen[end[0]][end[1]] is not None
            ):
                return True  ### Les deux derniers cas correspondent au cas où le pion mange une pièce (pas de prise en passant...)
            else:
                return False
        elif self.color == "white":
            if (
                start[0] == end[0]
                and start[1] - 1 == end[1]
                and screen[end[0]][end[1]] is None
            ):
                return True
            elif (
                start[0] == end[0]
                and start[1] - 2 == end[1]
                and start[1] == 1
                and screen[end[0]][end[1]] is None
            ):
                return True
            elif (
                start[0] + 1 == end[0]
                and start[1] - 1 == end[1]
                and screen[end[0]][end[1]] is not None
            ):
                return True
            elif (
                start[0] - 1 == end[0]
                and start[1] - 1 == end[1]
                and screen[end[0]][end[1]] is not None
            ):
                return True  ### Les deux derniers cas correspondent au cas où le pion mange une pièce (pas de prise en passant...)
            else:
                return False


class Rock(Piece):
    def coup_valide(self, start, end, screen):
        if start[0] == end[0] and start[1] != end[1]:
            if start[1] < end[1]:
                for i in range(start[1], end[1]):
                    if (
                        screen[start[0]][i] is not None
                    ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                        return False
                return True
            else:
                for i in range(end[1], start[1]):
                    if screen[start[0]][i] is not None:
                        return False
                return True
        elif start[0] != end[0] and start[1] == end[1]:
            if start[0] < end[0]:
                for i in range(start[0], end[0]):
                    if (
                        screen[start[0]][i] is not None
                    ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                        return False
                return True
            else:
                for i in range(end[0], start[0]):
                    if screen[start[0]][i] is not None:
                        return False
                return True
        return False


class Bishop(Piece):
    def coup_valide(self, start, end, screen):
        if (
            np.abs(start[0] - end[0]) == np.abs(start[1] - end[1])
        ):  ## Pour des déplcements en diagonale, on vérifie que la valeur absolue de la différence d'ordonnée est égale à la valeur np.absolue de la différence d'np.abscisse
            if (
                start[0] < end[0] and start[1] < end[1]
            ):  ## On différencie les cas possibles de déplacement selon les 4 diagonales (Haut-Droite, Bas-Droite, Haut-Gauche, Bas-Gauche)
                for i in range(1, np.abs(start[0] - end[0])):
                    if (
                        screen[start[0] + i][start[1] + i] is not None
                    ):  ## On vérifie qu'on ne rencontre aucune pièce sur le chemin
                        return False
                return True
            elif start[0] < end[0] and start[1] > end[1]:
                for i in range(1, np.abs(start[0] - end[0])):
                    if screen[start[0] + i][start[1] - i] is not None:
                        return False
                return True
            elif start[0] > end[0] and start[1] < end[1]:
                for i in range(1, np.abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] + i] is not None:
                        return False
                return True
            elif start[0] > end[0] and start[1] > end[1]:
                for i in range(1, np.abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] - i] is not None:
                        return False
                return True
        else:
            return False


class Knight(Piece):
    def coup_valide(self, start, end, screen):
        if (np.abs(start[0] - end[0]) == 2 and np.abs(start[1] - end[1]) == 1) or (
            np.abs(start[0] - end[0] == 1 and np.abs(start[1] - end[1]) == 2)
        ):
            return True  ## Le mouvement de L du cavalier correspond à un décalage de 1 case dans une direction et 2 cases dans une autre orthogonale à la 1ere, ce qui est effectivemetn traduit ici
        else:
            return False


class King(Piece):
    def coup_valide(self, start, end, screen):
        if np.abs(start[0] - end[0]) <= 1 and np.abs(start[1] - end[1]) <= 1:
            return True
        else:
            return False


class Queen(Piece):
    def coup_valide(self, start, end, screen):
        if (
            np.abs(start[0] - end[0]) == np.abs(start[1] - end[1])
        ):  ## Pour des déplcements en diagonale, on vérifie que la valeur np.absolue de la différence d'ordonnée est égale à la valeur np.absolue de la différence d'np.abscisse
            if (
                start[0] < end[0] and start[1] < end[1]
            ):  ## On différencie les cas possibles de déplacement selon les 4 diagonales (Haut-Droite, Bas-Droite, Haut-Gauche, Bas-Gauche)
                for i in range(1, np.abs(start[0] - end[0])):
                    if (
                        screen[start[0] + i][start[1] + i] is not None
                    ):  ## On vérifie qu'on ne rencontre aucune pièce sur le chemin
                        return False
                return True
            elif start[0] < end[0] and start[1] > end[1]:
                for i in range(1, np.abs(start[0] - end[0])):
                    if screen[start[0] + i][start[1] - i] is not None:
                        return False
                return True
            elif start[0] > end[0] and start[1] < end[1]:
                for i in range(1, np.abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] + i] is not None:
                        return False
                return True
            elif start[0] > end[0] and start[1] > end[1]:
                for i in range(1, np.abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] - i] is not None:
                        return False
                return True
        else:
            if start[0] == end[0] and start[1] != end[1]:
                if start[1] < end[1]:
                    for i in range(start[1], end[1]):
                        if (
                            screen[start[0]][i] is not None
                        ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                            return False
                    return True
                else:
                    for i in range(end[1], start[1]):
                        if screen[start[0]][i] is not None:
                            return False
                    return True
            elif start[0] != end[0] and start[1] == end[1]:
                if start[0] < end[0]:
                    for i in range(start[0], end[0]):
                        if (
                            screen[start[0]][i] is not None
                        ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                            return False
                    return True
                else:
                    for i in range(end[0], start[0]):
                        if screen[start[0]][i] is not None:
                            return False
                    return True
        return False


PB1 = Pawn("black", 0, 1)
PB2 = Pawn("black", 1, 1)
PB3 = Pawn("black", 2, 1)
PB4 = Pawn("black", 3, 1)
PB5 = Pawn("black", 4, 1)
PB6 = Pawn("black", 5, 1)
PB7 = Pawn("black", 6, 1)
PB8 = Pawn("black", 7, 1)
RB1 = Rock("black", 0, 0)
RB2 = Rock("black", 7, 0)
KB1 = Knight("black", 1, 0)
KB2 = Knight("black", 6, 0)
BB1 = Bishop("black", 2, 0)
BB2 = Bishop("black", 5, 0)
QB = Queen("black", 3, 0)
KB = King("black", 4, 0)
PW1 = Pawn("white", 0, 6)
PW2 = Pawn("white", 1, 6)
PW3 = Pawn("white", 2, 6)
PW4 = Pawn("white", 3, 6)
PW5 = Pawn("white", 4, 6)
PW6 = Pawn("white", 5, 6)
PW7 = Pawn("white", 6, 6)
PW8 = Pawn("white", 7, 6)
RW1 = Rock("white", 0, 7)
RW2 = Rock("white", 7, 7)
KW1 = Knight("white", 1, 7)
KW2 = Knight("white", 6, 7)
BW1 = Bishop("white", 2, 7)
BW2 = Bishop("white", 5, 7)
QW = Queen("white", 3, 7)
KW = King("white", 4, 7)

Pieces = [
    PB1,
    PB2,
    PB3,
    PB4,
    PB5,
    PB6,
    PB7,
    PB8,
    RB1,
    RB2,
    KB1,
    KB2,
    BB1,
    BB2,
    QB,
    KB,
    PW1,
    PW2,
    PW3,
    PW4,
    PW5,
    PW6,
    PW7,
    PW8,
    RW1,
    RW2,
    KW1,
    KW2,
    BW1,
    BW2,
    QW,
    KW,
]


def affichage(screen):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                col = (91, 60, 17)
                pg.draw.rect(ecran, col, (i * width, j * height, width, height))
            else:
                col = (169, 149, 123)
                pg.draw.rect(ecran, col, (i * width, j * height, width, height))

            # Si une pièce est présente dans la case, on la dessine
            piece = screen[i][j]
            if piece is not None:
                if isinstance(piece, Pawn):
                    if piece.color == "black":
                        pg.draw.circle(
                            ecran,
                            black,
                            (piece.x + width // 2, piece.y + height // 2),
                            15,
                        )
                    else:
                        pg.draw.circle(
                            ecran,
                            white,
                            (piece.x + width // 2, piece.y + height // 2),
                            15,
                        )
                elif isinstance(piece, Rock):
                    pg.draw.rect(
                        ecran,
                        black if piece.color == "black" else white,
                        (piece.x + 20, piece.y + 20, 40, 40),
                    )
                elif isinstance(piece, Knight):
                    pg.draw.polygon(
                        ecran,
                        black if piece.color == "black" else white,
                        [
                            (piece.x + 20, piece.y + 20),
                            (piece.x + 20, piece.y + 60),
                            (piece.x + 40, piece.y + 60),
                            (piece.x + 40, piece.y + 40),
                            (piece.x + 60, piece.y + 40),
                            (piece.x + 60, piece.y + 20),
                        ],
                    )
                elif isinstance(piece, Bishop):
                    pg.draw.rect(
                        ecran,
                        black if piece.color == "black" else white,
                        pg.Rect(piece.x + 30, piece.y + 10, 20, 60),
                    )
                elif isinstance(piece, Queen):
                    pg.draw.polygon(
                        ecran,
                        black if piece.color == "black" else white,
                        [
                            (piece.x + 20, piece.y + 40),
                            (piece.x + 40, piece.y + 20),
                            (piece.x + 60, piece.y + 40),
                            (piece.x + 40, piece.y + 60),
                        ],
                    )
                elif isinstance(piece, King):
                    pg.draw.polygon(
                        ecran,
                        black if piece.color == "black" else white,
                        [
                            (piece.x + 30, piece.y + 10),
                            (piece.x + 50, piece.y + 10),
                            (piece.x + 50, piece.y + 30),
                            (piece.x + 70, piece.y + 30),
                            (piece.x + 70, piece.y + 50),
                            (piece.x + 50, piece.y + 50),
                            (piece.x + 50, piece.y + 70),
                            (piece.x + 30, piece.y + 70),
                            (piece.x + 30, piece.y + 50),
                            (piece.x + 10, piece.y + 50),
                            (piece.x + 10, piece.y + 50),
                            (piece.x + 10, piece.y + 30),
                            (piece.x + 30, piece.y + 30),
                        ],
                    )


selected_piece = None

while running:
    clock.tick(5)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
        elif event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                x, y = pg.mouse.get_pos()
                start = [x // width, y // height]
                if screen[start[0]][start[1]] is not None:
                    selected_piece = screen[start[0]][start[1]]
            elif pg.mouse.get_pressed()[2]:
                x, y = pg.mouse.get_pos()
                end = [x // width, y // height]
                if selected_piece is not None:
                    if isinstance(selected_piece, Pawn) and selected_piece.coup_valide(
                        start, end, screen
                    ):
                        screen[end[0]][end[1]] = screen[start[0]][start[1]]
                        screen[start[0]][start[1]] = None
                        selected_piece.x = end[0] * width
                        selected_piece.y = end[1] * height
                    if isinstance(selected_piece, Rock) and selected_piece.coup_valide(
                        start, end, screen
                    ):
                        screen[end[0]][end[1]] = screen[start[0]][start[1]]
                        screen[start[0]][start[1]] = None
                        selected_piece.x = end[0] * width
                        selected_piece.y = end[1] * height
                    if isinstance(
                        selected_piece, Knight
                    ) and selected_piece.coup_valide(start, end, screen):
                        screen[end[0]][end[1]] = screen[start[0]][start[1]]
                        screen[start[0]][start[1]] = None
                        selected_piece.x = end[0] * width
                        selected_piece.y = end[1] * height
                    if isinstance(
                        selected_piece, Bishop
                    ) and selected_piece.coup_valide(start, end, screen):
                        screen[end[0]][end[1]] = screen[start[0]][start[1]]
                        screen[start[0]][start[1]] = None
                        selected_piece.x = end[0] * width
                        selected_piece.y = end[1] * height
                    if isinstance(selected_piece, Queen) and selected_piece.coup_valide(
                        start, end, screen
                    ):
                        screen[end[0]][end[1]] = screen[start[0]][start[1]]
                        screen[start[0]][start[1]] = None
                        selected_piece.x = end[0] * width
                        selected_piece.y = end[1] * height
                    if isinstance(selected_piece, King) and selected_piece.coup_valide(
                        start, end, screen
                    ):
                        screen[end[0]][end[1]] = screen[start[0]][start[1]]
                        screen[start[0]][start[1]] = None
                        selected_piece.x = end[0] * width
                        selected_piece.y = end[1] * height
            selected_piece = None

    ecran.fill((255, 255, 255))
    for i in range(8):
        for j in range(8):
            for piece in Pieces:
                if piece.x == i * width and piece.y == j * height:
                    screen[i][j] = piece

    affichage(screen)
    pg.display.update()
