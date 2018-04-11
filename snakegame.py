# Project: SnakeGame
#
# https://github.com/EnesGUL12/SnakeGame.git
#
# EnesGUL, dr-dobermann

import sys
import random
from math import ceil

import pygame
import pygame.locals


DD_LEFT  = 0
DD_RIGHT = 1
DD_UP    = 2
DD_DOWN  = 3

GS_NOT_STARTED = 0
GS_IN_PROGRESS = 1
GS_FINISHED    = 2
GS_PAUSED      = 3

GE_BERRY = 1
GE_EGG   = 2

SHIFT_CNTR = 4

EGG_TIME = 30 * 60
EGG_MAX_TIME = 10 * 60

SZ_SCREEN         = (1600, 900)
SZ_GRASS_PATT     = 160
SZ_WALL_PATT      = 40
SZ_WALL_W         = 80
SZ_WALL_H         = 40
SZ_S_OFFSET       = 55
SZ_STATE_SIZE     = 50
SZ_EGG_STATE_SIZE = 50

SZ_HEAD  = 20
SZ_BODY  = 20
SZ_BERRY = 15
SZ_EGG   = 20
SZ_STONE = SZ_BERRY
SZ_EYES  = 2

#TODO: Изменить цвета для того чтобы их было видно на траве
#TODO: Проработать плавные повороты змеи
#TODO: Найти картинки и подготовить картинки для тела змеи

C_BKGROUND = (  0,   0,   0)
C_BASE     = (153, 217, 234)
C_TEXT     = (128, 255,   0)
C_ST_LINE  = (255, 255,   0)

C_STONE    = ( 63,  63,  63)
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

#TODO: Создать стену на поле

class SnakeElem(FieldObj):
    def __init__(self, fld, dir, x, y, w, h):
        FieldObj.__init__(self, fld, x, y, w, h)
        self.direction = dir
        self.speed = 0 
        # Хранит точки изменения направления
        # Точки направления - [x, y, new_dir]
        self.ch_dir = []
        self.dd = 0
        self.image_body = pygame.image.load("./images/body.jpg")

    def SetDD(self, dd):
        self.dd = dd

    def Move(self, speed):
        self.speed = speed
        if self.direction == DD_RIGHT:
            dx = self.speed
            dy = 0
        elif self.direction == DD_LEFT:
            dx = -self.speed
            dy = 0
        elif self.direction == DD_UP:
            dx = 0
            dy = -self.speed
        elif self.direction == DD_DOWN:
            dx = 0
            dy = self.speed
        self.x += dx
        self.y += dy

        if self.x > self.field.w + self.field.x:
            self.x = 0
        if self.x < 0:
            self.x = self.field.w
        if self.y > self.field.h + self.field.y:
            self.y = self.field.y
        if self.y < self.field.y:
            self.y = self.field.h

        if len(self.ch_dir) == 0:
            return
        if self.x == self.ch_dir[0][0] and self.y == self.ch_dir[0][1]:
            self.direction = self.ch_dir[0][2]
            self.ch_dir.pop(0)

    def AddCDPoint(self, x, y, new_dir):
        self.ch_dir.append([x, y, new_dir])



class SnakeHead(SnakeElem):
    def __init__(self, dir, fld, x, y, w = SZ_HEAD, h = SZ_HEAD):
        SnakeElem.__init__(self, fld, dir, x, y, w, h)
        self.d = 1
        self.cntr = 0

    def Draw(self):
        # Нарисовать круг и две точки в качестве глаз
        x, y = self.x, self.y
        if self.direction == DD_DOWN or self.direction == DD_UP:
            x += self.dd
        if self.direction == DD_LEFT or self.direction == DD_RIGHT:
            y += self.dd
        pygame.draw.circle(self.field.screen, C_BERRY,
                           (x + int(SZ_HEAD/2), y + int(SZ_HEAD/2)),
                           int(SZ_HEAD / 2))
        if self.direction == DD_RIGHT or self.direction == DD_LEFT:
            # Нарисовать две точки глаз одна под другой(вертикально)
            pygame.draw.circle(self.field.screen, C_EYES,
                               (x + int(SZ_HEAD / 2),
                                y + int(SZ_HEAD / 3)), SZ_EYES)
            pygame.draw.circle(self.field.screen, C_EYES,
                               (x + int(SZ_HEAD / 2),
                                y + int(SZ_HEAD - (SZ_HEAD / 3))), SZ_EYES)
        else:
            # Нарисовать две точки глаз одну за другой(горизонтально)
            pygame.draw.circle(self.field.screen, C_EYES,
                               (x + int(SZ_HEAD / 3),
                                y + int(SZ_HEAD / 2)), SZ_EYES)
            pygame.draw.circle(self.field.screen, C_EYES,
                               (x + int(SZ_HEAD - (SZ_HEAD / 3)),
                                y + int(SZ_HEAD / 2)), SZ_EYES)

    def Move(self, speed):
        self.cntr += 1
        if self.cntr > SHIFT_CNTR:
            self.cntr = 0
            self.dd += self.d
        if self.dd > 1 or self.dd < -1:
            self.d = -self.d
        SnakeElem.Move(self, speed)



class SnakeBody(SnakeElem):
    def __init__(self, dir, fld, x, y, w = SZ_BODY, h = SZ_BODY):
        SnakeElem.__init__(self, fld, dir, x, y, w, h)

    def Draw(self):
        # Нарисовать жирную линию по направлению движения тела
        # Направление вправо или влево
        x, y = self.x, self.y
        if self.direction == DD_DOWN or self.direction == DD_UP:
            x += self.dd
        if self.direction == DD_LEFT or self.direction == DD_RIGHT:
            y += self.dd
        if self.direction == DD_RIGHT or self.direction == DD_LEFT:
            pygame.draw.line(self.field.screen, C_BODY,
                             (x, y + int(SZ_BODY/2)),
                             (x + SZ_BODY, y + int(SZ_BODY/2)), SZ_BODY)
        # Направление вверх или вниз
        elif self.direction == DD_UP or self.direction == DD_DOWN:
            pygame.draw.line(self.field.screen, C_BODY,
                             (x + int(SZ_HEAD/2), y),
                             (x + int(SZ_BODY / 2), y + SZ_BODY), SZ_BODY)



class SnakeTail(SnakeElem):
    def __init__(self, dir, fld, x, y, w = SZ_BODY, h = SZ_BODY):
        SnakeElem.__init__(self, fld, dir, x, y, w, h)

    def Draw(self):
        # Нарисовать пол-линии по направлению движения
        x, y = self.x, self.y
        if self.direction == DD_DOWN or self.direction == DD_UP:
            x += self.dd
        if self.direction == DD_LEFT or self.direction == DD_RIGHT:
            y += self.dd
        if self.direction == DD_RIGHT:
            x1 = x + int(SZ_BODY/2)
            x2 = x + SZ_BODY
            y1 = y + int(SZ_BODY/2)
            y2 = y1
        elif self.direction == DD_LEFT:
            x1 = x
            x2 = x + int(SZ_BODY/2)
            y1 = y + int(SZ_BODY/2)
            y2 = y1          
        elif self.direction == DD_UP:
            x1 = x + int(SZ_BODY/2)
            x2 = x1 
            y1 = y
            y2 = y + int(SZ_BODY/2)
        else:
            x1 = x + int(SZ_BODY/2)
            x2 = x1 
            y1 = y + int(SZ_BODY/2)
            y2 = y + SZ_BODY            
        pygame.draw.line(self.field.screen, C_BODY, (x1, y1),
                         (x2, y2), SZ_BODY) 
                    


class Snake(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, 0, 0)
        self.age = 0
        self.size = 3
        self.body = []
        self.speed = 2
        self.direction = DD_RIGHT
        self.MakeSnake()

    def Move(self):
        for i, e in enumerate(reversed(self.body)):
            if i < len(self.body) - 1:
                e.SetDD(self.body[len(self.body) - 2 - i].dd)
            e.Move(self.speed)
        
        # Проверить на пересечение прямогольников головы и ягодки
        rh = pygame.Rect(self.body[0].x, self.body[0].y,
                         self.body[0].w, self.body[0].h)
        rb = pygame.Rect(self.field.berry.x, self.field.berry.y,
                         self.field.berry.w, self.field.berry.h)
        if rh.colliderect(rb):
            self.field.ReplaceBerry()
            # Вставляем новую часть тела на место головы
            self.body.insert(1, SnakeBody(self.body[0].direction, self.field,
                                          self.body[0].x, self.body[0].y))
            # Переместим голову по направлению движения на размер головы
            if self.body[0].direction == DD_RIGHT:
                self.body[0].x += SZ_HEAD
            elif self.body[0].direction == DD_LEFT:
                self.body[0].x -= SZ_HEAD
            elif self.body[0].direction == DD_UP:
                self.body[0].y -= SZ_HEAD
            else:
                self.body[0].y += SZ_HEAD
            self.size += 1
            self.field.game.AddScore(GE_BERRY)
        # Проверить на пересечение прямоугольников голова и яйца
        if self.field.egg != None: 
            re = pygame.Rect(self.field.egg.x, self.field.egg.y, self.field.egg.w, self.field.egg.h)
            if rh.colliderect(re):
                self.field.EggEaten()
                self.field.game.AddScore(GE_EGG)
        # Проверить на пересечение прямогольников головы и камней
        ds = -1
        for i, s in enumerate(self.field.stones):
            rs = pygame.Rect(s.x, s.y, s.w, s.h)
            if rh.colliderect(rs):
                self.field.game.DecLife()
                ds = i
                break
        if ds != -1:
            self.field.RemoveStone(ds)
        # Проверить на пересечение прямогульников стены и головы
        rw = pygame.Rect(self.field.wall.x, self.field.wall.y, self.field.wall.w, self.field.wall.h)
        if rw.colliderect(rh):
            self.field.game.DecLife()
        # Проверить на пересечение прямоугольников стены и вишинки
        if rw.colliderect(rb):
            self.field.ReplaceBerry()
        # Проверить на пересечение прямоугольников стены и яйца
        if self.field.egg != None:
            if rw.colliderect(re):
                self.field.ReplaceWall()

        #TODO: Проверить на пересечение головы и частей тела


    def ChangeDir(self, dir):
        dir_constr = [set([DD_LEFT, DD_RIGHT]),
                      set([DD_DOWN, DD_UP])]
        for dc in dir_constr:    
            if self.direction in dc and dir in dc:
                return
        self.direction = dir
        self.body[0].direction = dir
        for e in self.body[1:]:
            e.AddCDPoint(self.body[0].x, self.body[0].y, dir)

    def MakeSnake(self):
        self.body.append(SnakeHead(self.direction, self.field, self.x, self.y))
        self.body.append(SnakeBody(self.direction, self.field, 
            self.x - SZ_BODY, self.y))
        self.body.append(SnakeTail(self.direction, self.field,
            self.x - 2 * SZ_BODY, self.y))

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
                           (self.x + int(SZ_STONE/2),
                            self.y + int(SZ_STONE/2)),
                           int(SZ_STONE/2))



class Berry(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_BERRY, SZ_BERRY)

    def Draw(self):
        # нарисовать кружок красного цвета
        pygame.draw.circle(self.field.screen, C_BERRY,
                           (self.x + int(SZ_BERRY/2),
                            self.y + int(SZ_BERRY/2)),
                           int(SZ_BERRY / 2))



class Wall(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_WALL_W, SZ_WALL_H)
        self.wall_image = pygame.image.load("./images/wall.jpg")

    def Draw(self):
        # Нарисовать стену
        for w in range(ceil(SZ_WALL_W / SZ_WALL_PATT)):
            for h in range(ceil(SZ_WALL_H / SZ_WALL_PATT)):
                self.field.screen.blit(self.wall_image, (self.x + SZ_WALL_PATT * w, self.y + SZ_WALL_PATT * h))

class Egg(FieldObj):
    def __init__(self, fld, x, y):
        FieldObj.__init__(self, fld, x, y, SZ_EGG, SZ_EGG)
        
    def Draw(self):
        # нарисовать круг белого цвета
        pygame.draw.circle(self.field.screen, C_EGG,
                   (self.x + int(SZ_EGG/2), self.y + int(SZ_EGG/2)),
                   int(SZ_EGG / 2))



class Field:
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.screen = self.game.screen
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.stones = []
        self.snake = None
        self.berry = None
        self.egg = None
        self.time = 0
        self.deltime = EGG_MAX_TIME
        self.grass = pygame.image.load("./images/grass1.jpg")
        self.wall = None

    def CreateField(self):
        # В случайных местах создать 6 камней и одну ягодy
        self.stones = []
        for s in range(6):
            x, y = random.randint(0, self.w), random.randint(0, self.h)
            self.stones.append(Stone(self, self.x + x, self.y + y))
        x, y = random.randint(0, self.w), random.randint(0, self.h)
        self.berry = Berry(self, self.x + x, self.y + y)
        # По центру экрана создать змею
        self.snake = Snake(self, self.x + int(self.w/2),
                           self.y + int(self.h/2))
        # Создать стену
        x, y = random.randint(100, self.w - 100), random.randint(SZ_STATE_SIZE, self.h - SZ_EGG_STATE_SIZE)
        self.wall = Wall(self, self.x + x, self.y + y)

    def Update(self):
        self.snake.Move()
        self.time += 1
        if self.time > EGG_TIME:
            self.time = 0
            if self.egg == None:
                x, y = random.randint(0, self.w), random.randint(0, self.h)
                self.egg = Egg(self, self.x + x, self.y + y)
                self.deltime = EGG_MAX_TIME
        if self.egg != None:
            self.game.DrawEggStat()
        # Удалить яйцо если находится на поле больше выделеного времени
        if self.egg != None:
            self.deltime -= 1
            if self.deltime == 0:
                self.egg = None

    def Draw(self):
        # Нарисовать фон
        for r in range(ceil(SZ_SCREEN[1]/SZ_GRASS_PATT)):
            for c in range(ceil(SZ_SCREEN[0]/SZ_GRASS_PATT)):
                self.screen.blit(self.grass, (c * SZ_GRASS_PATT, r * SZ_GRASS_PATT + SZ_STATE_SIZE))

        # Нарисовать все объекты
        for s in self.stones:
            s.Draw()

        # Нарисовать стену
        self.wall.Draw()

        # Нарисовать ягоду
        self.berry.Draw()

        # Нарисовать яйцо
        if self.egg != None:
            self.egg.Draw()

        # Нарисовать змею
        self.snake.Draw()
    
    def ReplaceBerry(self):
        # Удалить вишнеку и создать новую
        w, h = self.screen.get_size()
        x, y = random.randint(0, w), random.randint(0, h)
        self.berry = Berry(self, self.x + x, self.y + y)
        done = False
        rb = pygame.Rect(self.berry.x, self.berry.y, self.berry.w,
                         self.berry.h)

        while not done:
            for s in self.stones:
                rs = pygame.Rect(s.x, s.y, s.w, s.h)
                if rb.colliderect(rs):
                    x, y = random.randint(0, w), random.randint(0, h)
                    self.berry = Berry(self, x, y)
                else:
                    done = True
            for h in self.snake.body:
                rh = pygame.Rect(h.x, h.y, h.w, h.h)
                if rb.colliderect(rh):
                    x, y = random.randint(0, w), random.randint(0, h)
                    self.berry = Berry(self, x, y)
                else:
                    done = True


    def ReplaceWall(self):
        # Удалить вишнеку и создать новую
        x, y = random.randint(100, self.w - 100), random.randint(SZ_STATE_SIZE, self.h - SZ_EGG_STATE_SIZE)
        self.wall = Wall(self, self.x + x, self.y + y)        

    def EggEaten(self):
        self.egg = None
        self.time = 0

    def RemoveStone(self, si):
        self.stones.pop(si)



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.state = GS_NOT_STARTED
        self.lives = 3
        self.fld = Field(self, 0, SZ_STATE_SIZE, self.screen.get_width(),
                         self.screen.get_height() - SZ_STATE_SIZE)
    
    def Start(self):
        self.fld.CreateField()
        self.state = GS_IN_PROGRESS
        self.score = 0        
        self.lives = 3

    def ChangeDir(self, new_dir):
        if self.state == GS_IN_PROGRESS:
            self.fld.snake.ChangeDir(new_dir)

    def Update(self):
        if self.state == GS_IN_PROGRESS:
            self.fld.Update()
    
    def Draw(self):
        self.DrawStat()
        self.fld.Draw() 

    def DecLife(self):
        self.lives -= 1
        print("Lives count decremented to", self.lives)
        if self.lives == 0:
            self.Start()

    def DrawStat(self):
        s_rect = self.screen.get_rect()

        surf = self.screen.subsurface(pygame.Rect(0, 0,
                                 100, SZ_STATE_SIZE))
    
        font = pygame.font.SysFont("Consolas", 16, bold = True)


        bas     = font.render("Score[  ]",
                           True, C_BASE)

        score   = font.render("      " + str(self.score),
                           True, C_TEXT)

        surf.blit(bas, [10, 20])
        surf.blit(score, [10, 20])
        pygame.draw.line(self.screen, C_ST_LINE, (0, SZ_STATE_SIZE + 1),
                         (s_rect.w, SZ_STATE_SIZE + 1))
        x = 110
        for l in range(self.lives):
            life = SnakeHead(DD_DOWN, self.fld, x + l * (SZ_HEAD + 10), 20)
            life.Draw()
        
    def DrawEggStat(self):
        s_rect = self.screen.get_rect()
        surf = self.screen.subsurface(pygame.Rect(s_rect.w - 150,
                                                  0,
                                                  150, SZ_EGG_STATE_SIZE))
        font = pygame.font.SysFont("Consolas", 16, bold = True)
        bas  = font.render("Time left[    ]", True, C_BASE)
        time = font.render("          " + "{0:3.1f}".format(self.fld.deltime / 60), True, C_TEXT)

        surf.blit(bas, [10,20])
        surf.blit(time, [10,20])

    def AddScore(self, event):
        if event == GE_BERRY:
            self.score += 1
        elif event == GE_EGG:
            self.score += 5


def run():
    pygame.init()

    size = SZ_SCREEN
    screen=pygame.display.set_mode(size, pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake")
    # Добавить таймер чтобы обновление было не чаще чем 60 кадров в секунду
    clock = pygame.time.Clock()
    
    # Создать игру
    game = Game(screen)
    game.Start()
    
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Обработать нажатия клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True
                    break
                if event.key == pygame.K_RIGHT:
                    game.ChangeDir(DD_RIGHT)
                if event.key == pygame.K_LEFT:
                    game.ChangeDir(DD_LEFT)
                if event.key == pygame.K_UP:
                    game.ChangeDir(DD_UP)
                if event.key == pygame.K_DOWN:
                    game.ChangeDir(DD_DOWN)
        # --- Screen-clearing code goes here
        screen.fill(C_BKGROUND)
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        
        # --- Drawing code should go here
        game.Update()
        # Нарисовать поле
        game.Draw()

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()
    

if __name__ == "__main__":
    run()

