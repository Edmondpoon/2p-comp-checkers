import pygame
import ui
from constants import WINDOW, COLORS, WINNERS

pygame.init()






def generateScene(scene, winner = None):
    if scene == "END":
        bgImage = WINNERS[winner]

        PLAY_AGAIN = ui.textMaker("Play again?", COLORS["BLACK"], 50)
        twoP = ui.textMaker("Multiplayer", COLORS["BLACK"], 30)
        COMP = ui.textMaker("Computer", COLORS["BLACK"], 30)

        return bgImage, [(PLAY_AGAIN, (74, 50)), (twoP, (74, 50)), (COMP, (74, 50))]



def updateScene(*args):
        image, rectangles, texts = args


        WINDOW.fill(COLORS["WHITE"])
        WINDOW.blit(image, (0, 0))


        for rectangle in rectangles:
            ui.boxDesigner(WINDOW, COLORS["BLACK"], rectangle, (150, 100)) 


        for text in texts:
            ui.textDraw(WINDOW, text[0], text[1])



