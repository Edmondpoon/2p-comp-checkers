import pygame


pygame.init()



def textMaker(text, color, size):
    FONT = pygame.font.SysFont("comicsans", size)

    TEXT = FONT.render(text, True, color)
    return TEXT


def boxDesigner(window, color, position, size):
    pygame.draw.rect(window, color, position + size)


def textDraw(window, text, position):
    window.blit(text, position)
