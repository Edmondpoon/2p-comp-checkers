import pygame
from constants import COLORS, WINDOW, PIECE_SIZE, BLOCK_SIZE

pygame.init()


class Generator():
    
    @staticmethod
    def generateLines():
        for line in range(9):
            pygame.draw.line(WINDOW, COLORS["BLACK"], (10, (line * BLOCK_SIZE) + 90), (650, (line * BLOCK_SIZE) + 90))
            pygame.draw.line(WINDOW, COLORS["BLACK"], ((line * BLOCK_SIZE) + 10, 90), ((line * BLOCK_SIZE) + 10, 730))

    @staticmethod
    def generateBlock():
        for row in range(8):
            for column in range(8):
                if row % 2 == 0 and column % 2 != 0 and column != 0:
                    pygame.draw.rect(WINDOW, COLORS["GREEN"], ((column * BLOCK_SIZE) + 11, (row * BLOCK_SIZE) + 91, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
                elif row % 2 != 0 and row != 0 and column % 2 == 0:
                    pygame.draw.rect(WINDOW, COLORS["GREEN"], ((column * BLOCK_SIZE) + 11, (row * BLOCK_SIZE) + 91, BLOCK_SIZE - 1, BLOCK_SIZE - 1))



    @staticmethod
    def generateBoard():
        pygame.draw.rect(WINDOW, COLORS["GREY_WHITE"], (10, 90, 640, 640))
        Generator.generateLines()
        Generator.generateBlock()

    
    @staticmethod
    def generateGrid():
        grid = []
        for row in range(8):
            if row not in [3, 4] and row %2 == 0:
                grid.append([1 if (column != 0 and column % 2 != 0) else 0 for column in range(8)])
            elif row not in [3, 4] and row % 2 != 0:
                grid.append([1 if column % 2 == 0 else 0 for column in range(8)])
            else:
                grid.append([0 for column in range(8)])

        return grid


def generateBoard(p1, p2, clickedPiece, grid):
    WINDOW.fill(COLORS["WHITE"])


    Generator.generateBoard()

    for piece in p1.pieces + p2.pieces:
        piece.draw()

    if clickedPiece:
        clickedPiece.drawPossibleMoves(grid)
