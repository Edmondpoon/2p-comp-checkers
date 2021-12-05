import pygame
import comp_controls as cc
import scenes
import player
import pieces
from constants import WINDOW
import generate as gb


pygame.init()


def update():
    pygame.display.update()


def nextTurn(turn):
    return (turn + 1, None, False) 


def reset():
    return 


def checkerGame():
    RUN = True
    DEBUG = True
    END = None
    SECOND_PLAYER = None if not DEBUG else "comp"
    while True and not DEBUG:
        choice = input("Would you like to play against another player (2p) or the computer?")
        if choice in ["player", "computer"]:
            SECOND_PLAYER = "player" if choice == "player" else "comp"
            print("Have fun :)")
            break
        else:
            print("Invalid option. Please choose again.\n")


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

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        if END:
            generated_scene = False
            if not generated_scene:
                image, texts = scenes.generateScene("END", END)
                generated_scene = True

            scenes.updateScene(image, [], texts)
            update()
            if pygame.mouse.get_pressed()[0]:
                END = None
                generated_scene = False
                #FIXME choice to play with player or bot
            continue
        




        currentPlayer, nextPlayer = turns[turn % 2], turns[(turn + 1) % 2]

        if SECOND_PLAYER == "comp" and currentPlayer == p2:
            best_move = cc.decideMove(currentPlayer.pieces, grid, nextPlayer)
            chosen = None
            for piece in currentPlayer.remainingPieces:
                if piece.rowColumn == best_move[0][0]:
                    chosen = piece
                    break

            for move in best_move[0][1:]:
                chosen.move(move, grid)
            
            for pos in best_move[1]:
                for piece in nextPlayer.remainingPieces:
                    if piece.rowColumn == pos:
                        nextPlayer.remove(piece, grid)
                        break

            turn, clickedPiece, multiJump = nextTurn(turn)


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


        if not p1.pieces_left or not p2.pieces_left:
            END = "p1" if not p2.pieces_left else "p2"
        elif turn > 15:
            for p in [p1, p2]:
                if p.checkDraw(grid):
                    END = "draw"
                    break


        update()

        clock.tick(60)

    pygame.quit()



clock = pygame.time.Clock()
checkerGame()
