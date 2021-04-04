import pieces as p
import random
from constants import COLORS
import pygame


pygame.init()


def extraPoints(grid, piece, futurePos, pieces):
    row, col = piece.rowColumn
    fRow, fCol = futurePos
    checkSet1 = [[(1, -1), (-1, 1)], [(1, 1), (-1, -1)]]
    checkSet2 = [(1, -1), (1, -1)]
    points = 0

    for check in checkSet1:
        y1, x1, y2, x2 = check[0][0] + fRow, check[0][1] + fCol, check[1][0] + fRow, check[1][1] + fCol
        if not p.moveChecker.inBounds(y1, x1) or not p.moveChecker.inBounds(y2, x2):
            continue

        if grid[y1][x1] == 1 and p.moveChecker.checkPiece(y1, x1, COLORS["RED"], pieces):
            points -= 3
        
        if piece.kinged and grid[y2][x2] == 1 and p.moveChecker.checkPiece(y2, x2, COLORS["RED"], pieces):
            points -= 3

    for check in checkSet2:
        y1, x1 = check[0] + row, check[0] + col
        if not p.moveChecker.inBounds(y1, x1):
            continue

        if grid[y1][x1] == 1 and not p.moveChecker.checkPiece(y1, x1, COLORS["RED"], pieces):
            points -= 1
        

    for check in checkSet2:
        y1, x1 = check[0] + fRow, check[0] + fCol
        if not p.moveChecker.inBounds(y1, x1):
            continue

        if grid[y1][x1] == 1 and not p.moveChecker.checkPiece(y1, x1, COLORS["RED"], pieces):
            points += 2

    return points


def chain(row, column, grid, pieces, kinged, checked):
    temp = p.player2(row, column)
    temp.kinged = kinged
    moves = p.moveChecker.removable(temp, grid, pieces)

    for move in list(moves.keys()):
        if move in checked:
            del moves[move]

    keys = list(moves.keys())
    values = list(moves.values())
    temp_path = [[], []]
    temp_remove = [[value] for value in values]

    if not moves.keys() or not keys:
        return [(row, column)], []

    for move in range(len(keys)):
        checked.append(keys[move])
        recursive = chain(keys[move][0], keys[move][1], grid, pieces, kinged, checked)
        temp_path[move].extend(recursive[0])
        temp_remove[move].extend(recursive[1])


    return max(temp_path, key=len), max(temp_remove, key=len) 



def decideMove(pieces, grid, p1):
    paths = {}
    for piece in pieces:
        if not piece.taken:

            take, remove = chain(piece.row, piece.column, grid, pieces + p1.pieces, piece.kinged, [])
            moves = p.moveChecker.checkMoves(piece, grid, -1)
            take.insert(0, (piece.row, piece.column))
            extra_points = [extraPoints(grid, piece, move, pieces + p1.pieces) for move in moves]

            if len(set(take)) > 1:
                if len(take) * 5 in paths.keys():
                    paths[len(remove) * 5].append([take, remove])
                else:
                    paths[len(remove) * 5] = [[take, remove]]
            
            if len(moves) > 0:
                for move in range(len(moves)):
                    ep = extra_points[move]
                    length = len([(piece.row, piece.column), moves[move]])
                    if length + ep in paths.keys():
                        paths[length + ep].append([[(piece.row, piece.column), moves[move]], []])
                    else:
                        paths[length + ep] = [[[(piece.row, piece.column), moves[move]], []]]

    return random.choice(paths[max(list(paths.keys()))])
