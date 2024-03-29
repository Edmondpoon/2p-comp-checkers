from constants import PIECE_SIZE, WINDOW, COLORS, CROWN, MOVE_SIZE
import pygame

pygame.init()


class moveChecker():

    @staticmethod
    def inBounds(row, column):
        return 0 <= row < 8 and 0 <= column < 8

    @staticmethod
    def checkMoves(piece, grid, direction = None):
        Kdirection = piece.kingDirection if not direction else direction
        leftRight = {"left" : 1, "right" : -1}
        possibleMoves = []
        row, column = piece.row, piece.column
        for direction in leftRight.keys():
            if piece.kinged:
                if (moveChecker.inBounds(row + Kdirection, column + leftRight[direction])
                    and grid[row + Kdirection][column + leftRight[direction]] == 0):

                    possibleMoves.append((row + Kdirection, column + leftRight[direction]))

            if (moveChecker.inBounds(row + (-1 * Kdirection), column + leftRight[direction]) 
                    and grid[row + (Kdirection * -1)][column + leftRight[direction]] == 0):

                possibleMoves.append((row + (Kdirection * -1), column + leftRight[direction]))

        return possibleMoves

    @staticmethod
    def checkPiece(row, column, color, pieces):
        for piece in pieces:
            if piece.rowColumn == (row, column) and piece.color != color:
                return True

        return False


    @staticmethod
    def removable(piece, grid, pieces):
        Kdirection = piece.kingDirection
        playerPiece = piece.color
        leftRight = {"left" : 1, "right" : -1}
        possibleTakes = {}
        row, column = piece.row, piece.column
        for direction in leftRight.keys():
            if piece.kinged:
                if (moveChecker.inBounds(row + (Kdirection * 2), column + (2 * leftRight[direction])) 
                        and moveChecker.checkPiece(row + Kdirection, column + leftRight[direction], playerPiece, pieces) 
                        and grid[row + Kdirection][column + leftRight[direction]] == 1 
                        and grid[row + (2 * Kdirection)][column + (2 * leftRight[direction])] == 0):

                    possibleTakes[(row + (2 * Kdirection), column + (2 * leftRight[direction]))] =  (row + Kdirection, column + leftRight[direction])

            if (moveChecker.inBounds(row + (Kdirection * -2), column + (2 * leftRight[direction])) 
                    and moveChecker.checkPiece(row + (Kdirection * -1), column + leftRight[direction], playerPiece, pieces) 
                    and grid[row + (Kdirection * -1)][column + leftRight[direction]] == 1 
                    and grid[row + (-2 * Kdirection)][column + (2 * leftRight[direction])] == 0):

                possibleTakes[(row + (-2 * Kdirection), column + (2 * leftRight[direction]))] = (row + (Kdirection * -1), column + leftRight[direction])

        return possibleTakes



def generatePieces(player, grid):
    pieces = []
    if player == "player1":
        for row in range(8):
            for column in range(8):
                if row in range(5, 8) and grid[row][column] == 1:
                    pieces.append(player1(row, column))

    elif player == "player2":
        for row in range(8):
            for column in range(8):
                if row in range(3) and grid[row][column] == 1:
                    pieces.append(player2(row, column))

    return pieces


class piece():
    def __init__(self, row, column):
        self.kinged = False
        self.taken = False
        self.moves = None

        #characteristics
        self.size = PIECE_SIZE
        self.radius = self.size / 2

        #position
        self.row = row
        self.column = column

        #moves
        self.pTakes = {}
        self.pMoves = []

    @property
    def center(self):
        deltaY = self.row * 80
        deltaX = self.column * 80
        return (deltaX + 50, deltaY + 130)

    @property
    def pos(self):
        return self.center

    @property
    def rowColumn(self):
        return (self.row, self.column)

    def draw(self):
        center = self.center
        if self.kinged:
            pygame.draw.circle(WINDOW, self.color, center, self.radius)
            WINDOW.blit(CROWN, (center[0] - 22, center[1] - 15))
            return

        pygame.draw.circle(WINDOW, self.color, center, self.radius)


    def king(self):
        self.kinged = True

    def removePiece(self, grid):
        self.taken = True
        grid[self.row][self.column] = 0

    def move(self, pos, grid):
        grid[self.row][self.column] = 0
        grid[pos[0]][pos[1]] = 1
        self.row, self.column = pos[0], pos[1]

        if self.row == self.kingRow:
            self.king()

    def drawPossibleMoves(self, grid, pieces, multiJump):
        if not self.taken:
            possibleMoves = moveChecker.checkMoves(self, grid)
            possibleTakes = moveChecker.removable(self, grid, pieces)
            Moves = possibleMoves + list(possibleTakes.keys()) if not multiJump else list(possibleTakes.keys())

            for move in Moves:
                row, column = move
                center = ((column * 80) + 50, (row * 80) + 130)
                pygame.draw.circle(WINDOW, COLORS["GREY"], center, MOVE_SIZE / 2)
            self.pMoves = possibleMoves
            self.pTakes = possibleTakes
            

    def returnPossibleMoves(self):
        return self.pMoves

    def returnPossibleTakes(self):
        return self.pTakes

    def allMoves(self, grid, pieces):
        possibleMoves = moveChecker.checkMoves(self, grid)
        possibleTakes = moveChecker.removable(self, grid, pieces)
        return possibleMoves + list(possibleTakes.keys())

    def equal(self, pos):
        return self.rowColumn == pos


class player1(piece):
    def __init__(self, row, column):
        super().__init__(row, column)
        self.color = COLORS["WHITE"]
        self.kingDirection = 1
        self.kingRow = 0


class player2(piece):
    def __init__(self, xPos, yPos):
        super().__init__(xPos, yPos)
        self.color = COLORS["RED"]
        self.kingDirection = -1
        self.kingRow = 7
