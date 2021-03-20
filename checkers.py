import pygame
import player
import pieces
from constants import WINDOW
import generate as gb


pygame.init()


def update():
    pygame.display.update()


def nextTurn(turn):
    return (turn + 1, None, False) 






def checkerGame():
    RUN = True
    SECOND_PLAYER = "player"
    clickedPiece = None
    multiJump = False
    #FIXME: decide who second player is here

    #
    grid = gb.Generator.generateGrid()
    turn = 0

    #player
    p1_pieces = pieces.generatePieces("player1", grid)
    p2_pieces = pieces.generatePieces("player2", grid)
    p1 = player.Player(p1_pieces, grid)
    p2 = player.Player(p2_pieces, grid)
    turns = {0 : p1, 1 : p2}

    while RUN:
        currentPlayer, nextPlayer = turns[turn % 2], turns[(turn + 1) % 2]

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        if keys[pygame.K_LEFT]:
            print(grid)
            

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            row, column = (y // 80) - 1, (x // 80)

            if not 0 <= row <= 7 or not 0 <= column <= 7:
                pass

            elif grid[row][column] == 1 and not multiJump:
                for piece in currentPlayer.remainingPieces:
                    if piece.equal((row, column)):
                        clickedPiece = piece

            elif grid[row][column] == 0 and clickedPiece:
                if (row, column) in clickedPiece.returnPossibleMoves() and not multiJump:
                    clickedPiece.move((row, column), grid)
                    turn, clickedPiece, multiJump = nextTurn(turn)

                elif (row, column) in clickedPiece.returnPossibleTakes():
                    for piece in nextPlayer.remainingPieces:
                        if piece.equal(clickedPiece.returnPossibleTakes()[(row, column)]):
                            clickedPiece.move((row, column), grid)
                            nextPlayer.remove(piece, grid)
                            if pieces.moveChecker.removable(clickedPiece, grid, currentPlayer.pieces + nextPlayer.pieces):
                                multiJump = True

                            else:
                                turn, clickedPiece, multiJump = nextTurn(turn)

                            break


        gb.generateBoard(p1, p2, clickedPiece, grid, multiJump)



        update()

        clock.tick(60)

    pygame.quit()



clock = pygame.time.Clock()
checkerGame()
