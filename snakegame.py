# Project: SnakeGame
#
# https://github.com/EnesGUL12/SnakeGame.git
#
# EnesGUL, dr-dobermann

import pygame

C_BKGROUND = (0, 0, 0)

class Snake:
    def __init__(self):
        self.age = 0
        self.w = 20
        self.h = self.w
        self.size= 1
        self.x = 
        self.y = 
        self.speed = 

class Stone:
    def __init__(self):
        self.x = 
        self.y = 
        self.w = 20
        self.h = 25

class Berry:
    def __init__(self):
        self.w = 20
        self.h = 20
        self.x = 
        self.y = 

class Field:
    def __init__(self):
        self.snake = Snake
        self.stone = Stone



class Fish:
    def __init__(self):
        self.x = 
        self.y = 
        self.w = 25
        self.h = 30
        self.speed = 

class Water:
    def __init__(self):
        self.fish = Fish



def run():
    pygame.init()

    size=[800, 600]
    screen=pygame.display.set_mode(size, pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake")
    # Добавить таймер чтобы обновление было не чаще чем 60 кадров в секунду
    clock = pygame.time.Clock()
    
    
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
        # --- Screen-clearing code goes here
        screen.fill(C_BKGROUND)
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        
        # --- Drawing code should go here      

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()
    


run()

