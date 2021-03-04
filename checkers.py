import pygame
import network
import player
import pieces
from constants import WINDOW
import generate as gb


pygame.init()

clientNumber = 0

def update():
    pygame.display.update()


def checkerGame():
    RUN = True
    DEBUG_MODE = True
    SECOND_PLAYER = "player"
    clickedPiece = None
    #FIXME: decide who second player is here

    #
    grid = gb.Generator.generateGrid()
    turn = 1
    p1_left = 12
    p2_left = 12

    #player
    if SECOND_PLAYER == "player":
        n = network.Network()
        p1 = n.getPlayer()

    else:
        p1_pieces = pieces.generatePieces("player1", grid)
        p2_pieces = pieces.generatePieces("player2", grid)
        p1 = player.Player(p1_pieces, grid)
        p2 = player.Player(p2_pieces, grid)

    while RUN:
        if SECOND_PLAYER == "player":
            p2 = n.send(p1)
            #p1.grid = p2.grid


        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        if keys[pygame.K_LEFT]:
            print(p1.grid, 'palyer1')
            print(p2.grid, 'player2')

        if DEBUG_MODE and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            #print("Current mouse position:", x,y)

        #how to remove piece from both things
        #p1.pieceRemove(piece, grid)
        if pygame.mouse.get_pressed()[0]:
            #find the piece associated with the click and assign to clickedPiece
            x, y = pygame.mouse.get_pos()
            row = (y // 80) - 1
            column = (x // 80)
#            if row < 0 or column < 0:
 #               pass
  #          elif grids[p1.player][row][column] == 1:
   #             for piece in p1.remainingPieces + p2.remainingPieces:
    #                if piece.row == row and piece.column == column:
     #                   clickedPiece = piece
      #      elif grids[p1.player][row][column] == 0 and clickedPiece:
       #         if (row, column) in clickedPiece.returnPossibleMoves():
        #            clickedPiece.move((row, column), p1, p2)
                #elif (row, column) in clickedPiece.returnPossibleTakes():

                    


        gb.generateBoard(p1, p2, clickedPiece, grid)



        update()

        clock.tick(60)

    pygame.quit()



clock = pygame.time.Clock()
checkerGame()
