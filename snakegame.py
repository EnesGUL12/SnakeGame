# Project: SnakeGame
#
# https://github.com/EnesGUL12/SnakeGame.git
#
# EnesGUL, dr-dobermann

import random

import pygame

C_BKGROUND = (0, 0, 0)

DD_LEFT  = 0
DD_RIGHT = 1
DD_UP    = 2
DD_DOWN  = 3

SZ_HEAD  = 20
SZ_BODY  = 10
SZ_BERRY = 15
SZ_EGG   = 20


class FieldObj:
    def __init__(self, fld, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.field = fld

    def Draw(self):
        pass

class SnakeHead(FieldObj):
    def __init__(self, dir, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_HEAD, SZ_HEAD)
        self.direction = dir

    def Draw(self):
        # Нарисовать круг и две точки в качестве глаз
        pass

class SnakeBody(FieldObj):
    def __init__(self, dir, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_BODY, SZ_BODY)
        self.direction = dir

    def Draw(self):
        # Нарисовать жирную линию по направлению движения тела
        pass

class SnakeTail(FieldObj):
        def __init__(self, dir, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_BODY, SZ_BODY)
        self.direction = dir

    def Draw(self):
        # Нарисовать пол-линии по направлению движения

class Snake(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, 0, 0)
        self.age = 0
        self.size = 3
        self.body = []
        self.speed = 0
        self.MakeSnake()

    def MakeSnake(self):
        self.body.append(SnakeHead(DD_RIGHT, self.field, self.x, self.y))
        self.body.append(SnakeBody(DD_RIGHT, self.field, 
            self.x - SZ_BODY, self.y + int((SZ_HEAD - SZ_BODY)/2)))
        self.body.append(SnakeTail(DD_RIGHT, self.field,
            self.x - 2 * SZ_BODY, self.y + int((SZ_HEAD - SZ_BODY)/2)))

    def Draw(self):
        for b in self.body:
            b.Draw()


class Stone(FieldObj):
    def __init__(self, fld, x, y):
        size = random.randint(10, 50)
        FieldObj.__init__(self, fld, x, y, size, size)
    
    def Draw(self):
        # Нарисовать закрашенный круг
        pass

class Berry(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_BERRY, SZ_BERRY)

    def Draw(self):
        # нарисовать кружок красного цвета
        pass 

class Egg(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_EGG, SZ_EGG)
        
    def Draw(self):
        # нарисовать круг белого цвета
        pass

class Field:
    def __init__(self, screen, x, y, w, h):
        self.screen = screen
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.fldObj = []
        self.snake = None

    def CreateField(self):
        # В случайных местах создать 6 камней и одну ягоду
        # По центру экрана создать змею
        pass

    def Draw(self):
        # Нарисовать фон
        # Нарисовать все объекты
        # Нарисовать змею
        pass


def run():
    pygame.init()

    size=[800, 600]
    screen=pygame.display.set_mode(size, pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake")
    # Добавить таймер чтобы обновление было не чаще чем 60 кадров в секунду
    clock = pygame.time.Clock()
    
    # Создать поле
    
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
        # Нарисовать поле

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()
    


run()

