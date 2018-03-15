# Project: SnakeGame
#
# https://github.com/EnesGUL12/SnakeGame.git
#
# EnesGUL, dr-dobermann

import random

import pygame
import pygame.locals


DD_LEFT  = 0
DD_RIGHT = 1
DD_UP    = 2
DD_DOWN  = 3

SZ_HEAD  = 20
SZ_BODY  = 13
SZ_TAIL  = SZ_BODY / 2
SZ_BERRY = 15
SZ_EGG   = 20
SZ_STONE = SZ_BERRY
SZ_EYES  = 2

C_BKGROUND = (  0,   0,   0)
C_STONE    = (127, 127, 127)
C_BERRY    = (181,  30,  30)
C_EGG      = (255, 255, 255)
C_BODY     = (  0, 198,  50)
C_EYES     = (  0, 162, 232)

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
        pygame.draw.circle(self.field.screen, C_BERRY,
                           (self.x + int(SZ_HEAD/2), self.y + int(SZ_HEAD/2)),
                           int(SZ_HEAD / 2))
        if self.direction == DD_RIGHT or self.direction == DD_LEFT:
            # Нарисовать две точки глаз одна под другой(вертикально)
            pygame.draw.circle(self.field.screen, C_EYES,
                               (self.x + int(SZ_HEAD / 2), self.y + int(SZ_HEAD / 3)), SZ_EYES)
            pygame.draw.circle(self.field.screen, C_EYES,
                               (self.x + int(SZ_HEAD / 2), self.y + int(SZ_HEAD - (SZ_HEAD / 3))), SZ_EYES)
        else:
            # Нарисовать две точки глаз одну за другой(горизонтально)
            pygame.draw.line(self.field.screen, C_EYES,
                             (self.x + int(SZ_HEAD / 3), self.y + int(SZ_HEAD / 2)), SZ_EYES)
            pygame.draw.line(self.field.screen, C_EYES,
                             (self.x + int(SZ_HEAD - (SZ_HEAD / 3)), self.y + int(SZ_HEAD / 2)), SZ_EYES)
 

class SnakeBody(FieldObj):
    def __init__(self, dir, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_BODY, SZ_BODY)
        self.direction = dir

    def Draw(self):
        # Нарисовать жирную линию по направлению движения тела
        # Направление вправо
        if self.direction == DD_RIGHT:
            pygame.draw.line(self.field.screen, C_BODY, (self.x, self.y + int(SZ_BODY/2)),
                             (self.x - SZ_BODY, self.y + int(SZ_BODY/2)), SZ_BODY)
        # Направление влево
        elif self.direction == DD_LEFT:
            pygame.draw.line(self.field.screen, C_BODY, (self.x + SZ_HEAD, self.y + int(SZ_BODY/2)),
                             (self.x + (SZ_BODY + SZ_HEAD), self.y + int(SZ_BODY/2)), SZ_BODY)
        # Направление вверх
        elif self.direction == DD_UP:
            pygame.draw.line(self.field.screen, C_BODY, (self.x + int(SZ_HEAD/2), self.y + SZ_HEAD),
                             (self.x + int(SZ_BODY / 2), self.y + (SZ_HEAD + SZ_BODY), SZ_BODY))
        # Направление вниз
        else:
            pygame.draw.line(self.field.screen, C_BODY, (self.x + int(SZ_HEAD/2), self.y),
                             (self.x + int(SZ_BODY / 2), self.y - SZ_BODY), SZ_BODY)



class SnakeTail(FieldObj):
    def __init__(self, dir, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_BODY, SZ_BODY)
        self.direction = dir

    def Draw(self):
        # Нарисовать пол-линии по направлению движения
        if self.direction == DD_RIGHT:
            pygame.draw.line(self.field.screen, C_BODY, (self.x - SZ_BODY, self.y + int(SZ_BODY/2)),
            (self.x - SZ_BODY - SZ_TAIL, self.y + int(SZ_BODY/2)), SZ_BODY)
        elif self.direction == DD_LEFT:
            pygame.draw.line(self.field.screen, C_BODY, (self.x + SZ_HEAD + SZ_BODY, self.y + int(SZ_BODY/2)),
            (self.x + SZ_HEAD + SZ_BODY + SZ_TAIL, self.y + int(SZ_BODY/2)), SZ_BODY)
        elif self.direction == DD_UP:
            pygame.draw.line(self.field.screen, C_BODY, (self.x + int(SZ_HEAD / 2), self.y + SZ_HEAD + SZ_BODY),
            (self.x + int(SZ_BODY/2), self.y + SZ_BODY + SZ_HEAD + SZ_TAIL), SZ_BODY) 
        else:
            pygame.draw.line(self.field.screen, C_BODY, (self.x + int(SZ_HEAD / 2), self.y - SZ_BODY),
            (self.x + int(SZ_BODY/2), self.y - SZ_HEAD - SZ_TAIL), SZ_BODY) 
            


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
        pygame.draw.circle(self.field.screen, C_STONE,
                           (self.x + int(SZ_STONE/2), self.y + int(SZ_STONE/2)), 
                           int(SZ_STONE/2))

class Berry(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_BERRY, SZ_BERRY)

    def Draw(self):
        # нарисовать кружок красного цвета
        pygame.draw.circle(self.field.screen, C_BERRY,
                           (self.x + int(SZ_BERRY/2), self.y + int(SZ_BERRY/2)), 
                           int(SZ_BERRY / 2))
        

class Egg(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_EGG, SZ_EGG)
        
    def Draw(self):
        # нарисовать круг белого цвета
        pygame.draw.circle(self.field.screen, C_EGG,
                   (self.x + int(SZ_EGG/2), self.y + int(SZ_EGG/2)),
                   int(SZ_EGG / 2))


class Field:
    def __init__(self, screen, x, y, w, h):
        self.screen = screen
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.stones = []
        self.snake = None
        self.berry = None

    def CreateField(self):
        w, h = self.screen.get_size()
        # В случайных местах создать 6 камней и одну ягодy
        for s in range(6):
            x, y = random.randint(0, w), random.randint(0, h)
            self.stones.append(Stone(self, x, y))
        x, y = random.randint(0, w), random.randint(0, h)
        self.berry = Berry(self, x, y)
        # По центру экрана создать змею
        self.snake = Snake(self, int(w/2), int(h/2))

    def Draw(self):
        # Нарисовать фон
        # Нарисовать все объекты
        for s in self.stones:
            s.Draw()

        # Нарисовать ягоду
        self.berry.Draw()

        # Нарисовать змею
        self.snake.Draw()


def run():
    pygame.init()

    size=[1600, 900]
    screen=pygame.display.set_mode(size, pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake")
    # Добавить таймер чтобы обновление было не чаще чем 60 кадров в секунду
    clock = pygame.time.Clock()
    
    # Создать поле
    fld = Field(screen, 0, 0, screen.get_width(), screen.get_height())
    fld.CreateField()
    
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Обработать нажатия клавиш
            if event.type == pygame.KEYDOWN:
                if event.type == K_BACKSPACE:
                    done = True
                    continue
    
        # --- Screen-clearing code goes here
        screen.fill(C_BKGROUND)
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        
        # --- Drawing code should go here      
        # Нарисовать поле
        fld.Draw()

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()
    

if __name__ == "__main__":
    run()

