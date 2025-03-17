import pygame as pg
import random as rd

pg.init()
width = 80
height = 80
size = 8
screen = pg.display.set_mode((width * size, height * size))
running = True
clock = pg.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)


class Piece:
    def __init__(self, color, n, m):
        self.color = color
        self.x = n * width
        self.y = m * height

    def coup_valide(self, start, end, screen):
        pass


class Pawn(Piece):
    def coup_valide(self, start, end, screen):
        if self.color == "black":
            if (
                start[0] == end[0]
                and start[1] + 1 == end[1]
                and screen[end[0]][end[1]] == None
            ):
                return True
            elif (
                start[0] == end[0]
                and start[1] + 2 == end[1]
                and start[1] == 1
                and screen[end[0]][end[1]] == None
            ):
                return True
            elif (
                start[0] + 1 == end[0]
                and start[1] + 1 == end[1]
                and screen[end[0]][end[1]] != None
            ):
                return True
            elif (
                start[0] - 1 == end[0]
                and start[1] + 1 == end[1]
                and screen[end[0]][end[1]] != None
            ):
                return True  ### Les deux derniers cas correspondent au cas où le pion mange une pièce (pas de prise en passant...)
            else:
                return False
        elif self.color == "white":
            if (
                start[0] == end[0]
                and start[1] - 1 == end[1]
                and screen[end[0]][end[1]] == None
            ):
                return True
            elif (
                start[0] == end[0]
                and start[1] - 2 == end[1]
                and start[1] == 1
                and screen[end[0]][end[1]] == None
            ):
                return True
            elif (
                start[0] + 1 == end[0]
                and start[1] - 1 == end[1]
                and screen[end[0]][end[1]] != None
            ):
                return True
            elif (
                start[0] - 1 == end[0]
                and start[1] - 1 == end[1]
                and screen[end[0]][end[1]] != None
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
                        screen[start[0]][i] != None
                    ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                        return False
                return True
            else:
                for i in range(end[1], start[1]):
                    if screen[start[0]][i] != None:
                        return False
                return True
        elif start[0] != end[0] and start[1] == end[1]:
            if start[0] < end[0]:
                for i in range(start[0], end[0]):
                    if (
                        screen[start[0]][i] != None
                    ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                        return False
                return True
            else:
                for i in range(end[0], start[0]):
                    if screen[start[0]][i] != None:
                        return False
                return True
        return False


class Bishop(Piece):
    def coup_valide(self, start, end, screen):
        if (
            abs(start[0] - end[0]) == abs(start[1] - end[1])
        ):  ## Pour des déplcements en diagonale, on vérifie que la valeur absolue de la différence d'ordonnée est égale à la valeur absolue de la différence d'abscisse
            if (
                start[0] < end[0] and start[1] < end[1]
            ):  ## On différencie les cas possibles de déplacement selon les 4 diagonales (Haut-Droite, Bas-Droite, Haut-Gauche, Bas-Gauche)
                for i in range(1, abs(start[0] - end[0])):
                    if (
                        screen[start[0] + i][start[1] + i] != None
                    ):  ## On vérifie qu'on ne rencontre aucune pièce sur le chemin
                        return False
                return True
            elif start[0] < end[0] and start[1] > end[1]:
                for i in range(1, abs(start[0] - end[0])):
                    if screen[start[0] + i][start[1] - i] != None:
                        return False
                return True
            elif start[0] > end[0] and start[1] < end[1]:
                for i in range(1, abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] + i] != None:
                        return False
                return True
            elif start[0] > end[0] and start[1] > end[1]:
                for i in range(1, abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] - i] != None:
                        return False
                return True
        else:
            return False


class Knight(Piece):
    def coup_valide(self, start, end, screen):
        if (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 1) or (
            abs(start[0] - end[0] == 1 and abs(start[1] - end[1]) == 2)
        ):
            return True  ## Le mouvement de L du cavalier correspond à un décalage de 1 case dans une direction et 2 cases dans une autre orthogonale à la 1ere, ce qui est effectivemetn traduit ici
        else:
            return False


class King(Piece):
    def coup_valide(self, start, end, screen):
        if abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1:
            return True
        else:
            return False


class Queen(Piece):
    def coup_valide(self, start, end, screen):
        if (
            abs(start[0] - end[0]) == abs(start[1] - end[1])
        ):  ## Pour des déplcements en diagonale, on vérifie que la valeur absolue de la différence d'ordonnée est égale à la valeur absolue de la différence d'abscisse
            if (
                start[0] < end[0] and start[1] < end[1]
            ):  ## On différencie les cas possibles de déplacement selon les 4 diagonales (Haut-Droite, Bas-Droite, Haut-Gauche, Bas-Gauche)
                for i in range(1, abs(start[0] - end[0])):
                    if (
                        screen[start[0] + i][start[1] + i] != None
                    ):  ## On vérifie qu'on ne rencontre aucune pièce sur le chemin
                        return False
                return True
            elif start[0] < end[0] and start[1] > end[1]:
                for i in range(1, abs(start[0] - end[0])):
                    if screen[start[0] + i][start[1] - i] != None:
                        return False
                return True
            elif start[0] > end[0] and start[1] < end[1]:
                for i in range(1, abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] + i] != None:
                        return False
                return True
            elif start[0] > end[0] and start[1] > end[1]:
                for i in range(1, abs(start[0] - end[0])):
                    if screen[start[0] - i][start[1] - i] != None:
                        return False
                return True
        else:
            if start[0] == end[0] and start[1] != end[1]:
                if start[1] < end[1]:
                    for i in range(start[1], end[1]):
                        if (
                            screen[start[0]][i] != None
                        ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                            return False
                    return True
                else:
                    for i in range(end[1], start[1]):
                        if screen[start[0]][i] != None:
                            return False
                    return True
            elif start[0] != end[0] and start[1] == end[1]:
                if start[0] < end[0]:
                    for i in range(start[0], end[0]):
                        if (
                            screen[start[0]][i] != None
                        ):  ### On vérifie que les cases sur lesquelles se déplacent la tour ne contiennent pas dejà de pièces
                            return False
                    return True
                else:
                    for i in range(end[0], start[0]):
                        if screen[start[0]][i] != None:
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


def mouvement(Piece, start, end, screen):
    if Piece.coup_valide():
        screen[end[0]][end[1]] = screen[start[0]][
            start[1]
        ]  ###Normalement si une pièce se trouve en position end[0], end[1], elle est alors supprimée de screen car "mangée" par la pièce qui arrive en cette position
        screen[start[0]][start[1]] = None
    else:
        return "coup illegal"


def affichage(screen):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                col = (91, 60, 17)
                pg.draw.rect(screen, col, (i * size, j * size, size, size))
            else:
                pg.draw.rect(screen, black, (i * size, j * size, size, size))
            if screen[i][j] != None:
                if screen[i][j] == "PB1":
                    pg.draw.circle(screen, black, (PB1.x + 40, PB1.y + 40), 15)
                elif screen[i][j] == "PB2":
                    pg.draw.circle(screen, black, (PB2.x + 40, PB2.y + 40), 15)
                elif screen[i][j] == "PB3":
                    pg.draw.circle(screen, black, (PB3.x + 40, PB3.y + 40), 15)
                elif screen[i][j] == "PB4":
                    pg.draw.circle(screen, black, (PB4.x + 40, PB4.y + 40), 15)
                elif screen[i][j] == "PB5":
                    pg.draw.circle(screen, black, (PB5.x + 40, PB5.y + 40), 15)
                elif screen[i][j] == "PB6":
                    pg.draw.circle(screen, black, (PB6.x + 40, PB6.y + 40), 15)
                elif screen[i][j] == "PB7":
                    pg.draw.circle(screen, black, (PB7.x + 40, PB7.y + 40), 15)
                elif screen[i][j] == "PB8":
                    pg.draw.circle(screen, black, (PB8.x + 40, PB8.y + 40), 15)
                elif screen[i][j] == "RB1":
                    pg.draw.rect(screen, black, (RB1.x, RB1.y, width, height))
                elif screen[i][j] == "RB2":
                    pg.draw.rect(screen, black, (RB2.x, RB2.y, width, height))
                elif screen[i][j] == "KB1":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (KB1.x + 20, KB1.y + 20),
                            (KB1.x + 20, KB1.y + 60),
                            (KB1.x + 40, KB1.y + 60),
                            (KB1.x + 40, KB1.y + 40),
                            (KB1.x + 60, KB1.y + 40),
                            (KB1.x + 60, KB1.y + 20),
                        ],
                    )
                elif screen[i][j] == "KB2":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (KB2.x + 20, KB2.y + 20),
                            (KB2.x + 20, KB2.y + 60),
                            (KB2.x + 40, KB2.y + 60),
                            (KB2.x + 40, KB2.y + 40),
                            (KB2.x + 60, KB2.y + 40),
                            (KB2.x + 60, KB2.y + 20),
                        ],
                    )
                elif screen[i][j] == "BB1":
                    pg.draw.rect(screen, black, pg.Rect(BB1.x + 30, BB1.y + 10, 20, 60))
                elif screen[i][j] == "BB2":
                    pg.draw.rect(screen, black, pg.Rect(BB2.x + 30, BB2.y + 10, 20, 60))
                elif screen[i][j] == "QB":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (QB.x + 20, QB.y + 40),
                            (QB.x + 40, QB.y + 20),
                            (QB.x + 60, QB.y + 40),
                            (QB.x + 40, QB.y + 60),
                        ],
                    )
                elif screen[i][j] == "KB":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (KB.x + 30, KB.y + 10),
                            (KB.x + 50, KB.y + 10),
                            (KB.x + 50, KB.y + 30),
                            (KB.x + 70, KB.y + 30),
                            (KB.x + 70, KB.y + 50),
                            (KB.x + 50, KB.y + 50),
                            (KB.x + 50, KB.y + 70),
                            (KB.x + 30, KB.y + 70),
                            (KB.x + 30, KB.y + 50),
                            (KB.x + 10, KB.y + 50),
                            (KB.x + 10, KB.y + 50),
                            (KB.x + 10, KB.y + 30),
                            (KB.x + 30, KB.y + 30),
                        ],
                    )

                if screen[i][j] == "PW1":
                    pg.draw.circle(screen, black, (PW1.x + 40, PW1.y + 40), 15)
                elif screen[i][j] == "PW2":
                    pg.draw.circle(screen, black, (PW2.x + 40, PW2.y + 40), 15)
                elif screen[i][j] == "PW3":
                    pg.draw.circle(screen, black, (PW3.x + 40, PW3.y + 40), 15)
                elif screen[i][j] == "PW4":
                    pg.draw.circle(screen, black, (PW4.x + 40, PW4.y + 40), 15)
                elif screen[i][j] == "PW5":
                    pg.draw.circle(screen, black, (PW5.x + 40, PW5.y + 40), 15)
                elif screen[i][j] == "PW6":
                    pg.draw.circle(screen, black, (PW6.x + 40, PW6.y + 40), 15)
                elif screen[i][j] == "PW7":
                    pg.draw.circle(screen, black, (PW7.x + 40, PW7.y + 40), 15)
                elif screen[i][j] == "PW8":
                    pg.draw.circle(screen, black, (PW8.x + 40, PW8.y + 40), 15)
                elif screen[i][j] == "RW1":
                    pg.draw.rect(screen, black, (RW1.x, RW1.y, width, height))
                elif screen[i][j] == "RW2":
                    pg.draw.rect(screen, black, (RW2.x, RW2.y, width, height))
                elif screen[i][j] == "KW1":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (KW1.x + 20, KW1.y + 20),
                            (KW1.x + 20, KW1.y + 60),
                            (KW1.x + 40, KW1.y + 60),
                            (KW1.x + 40, KW1.y + 40),
                            (KW1.x + 60, KW1.y + 40),
                            (KW1.x + 60, KW1.y + 20),
                        ],
                    )
                elif screen[i][j] == "KW2":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (KW2.x + 20, KW2.y + 20),
                            (KW2.x + 20, KW2.y + 60),
                            (KW2.x + 40, KW2.y + 60),
                            (KW2.x + 40, KW2.y + 40),
                            (KW2.x + 60, KW2.y + 40),
                            (KW2.x + 60, KW2.y + 20),
                        ],
                    )
                elif screen[i][j] == "BW1":
                    pg.draw.rect(screen, black, pg.Rect(BW1.x + 30, BW1.y + 10, 20, 60))
                elif screen[i][j] == "BW2":
                    pg.draw.rect(screen, black, pg.Rect(BW2.x + 30, BW2.y + 10, 20, 60))
                elif screen[i][j] == "QW":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (QW.x + 20, QB.y + 40),
                            (QW.x + 40, QW.y + 20),
                            (QW.x + 60, QW.y + 40),
                            (QW.x + 40, QW.y + 60),
                        ],
                    )
                elif screen[i][j] == "KW":
                    pg.draw.polygon(
                        screen,
                        black,
                        [
                            (KW.x + 30, KB.y + 10),
                            (KW.x + 50, KW.y + 10),
                            (KW.x + 50, KW.y + 30),
                            (KW.x + 70, KW.y + 30),
                            (KW.x + 70, KW.y + 50),
                            (KW.x + 50, KW.y + 50),
                            (KW.x + 50, KW.y + 70),
                            (KW.x + 30, KW.y + 70),
                            (KW.x + 30, KW.y + 50),
                            (KW.x + 10, KW.y + 50),
                            (KW.x + 10, KW.y + 50),
                            (KW.x + 10, KW.y + 30),
                            (KW.x + 30, KW.y + 30),
                        ],
                    )


while running:
    clock.tick(10)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
        elif event.type == pg.QUIT:
            running = False
    screen.fill((255, 255, 255))
