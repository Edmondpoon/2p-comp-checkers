import pygame
pygame.init()

#window
HEIGHT = 740
WIDTH = 660
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#crown
CROWN = pygame.transform.scale(pygame.image.load("images/crown.png"), (44, 26))

#winner images
WINNERS = {
"p1" : pygame.transform.scale(pygame.image.load("images/p1Win.png"), (740, 660)),
"p2" : pygame.transform.scale(pygame.image.load("images/p2Win.png"), (740, 660)),
"draw" : pygame.transform.scale(pygame.image.load("images/draw.png"), (740, 660)),
}


#colors
COLORS = {
"GREEN" : (40, 100, 40),
"GREY_WHITE" : (255, 255, 224),
"WHITE" : (255, 255, 255),
"BLACK" : (0, 0, 0),
"RED" : (255, 0, 0),
"GREY" : (128, 128, 128),
}

#sizes
BLOCK_SIZE = 80
PIECE_SIZE = 60
MOVE_SIZE = 42
# board width is 10 - 650
# board height is 90 - 730 


