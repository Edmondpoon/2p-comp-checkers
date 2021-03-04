import pygame

pygame.init()


class Player():
    def __init__(self, pieces, grid):
        self.pieces = pieces
        self.pieces_left = 12
        self.grid = grid
        self.player = self.pieces[0].color


    @property
    def positions(self):
        return self.pieces


    def pieceRemove(self, piece, grid):
        self.pieces_left -= 1
        piece.pieceRemove(grid)

    @property
    def remainingPieces(self):
        return [piece for piece in self.pieces if not piece.taken]
