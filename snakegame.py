# Project: SnakeGame
#
# https://github.com/EnesGUL12/SnakeGame.git
#
# EnesGUL, dr-dobermann

import pygame

C_BKGROUND = (0, 0, 0)



def run():
    pygame.init()

    size=[800, 600]
    screen=pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
        screen.fill(C_BKGROUND)



run()

