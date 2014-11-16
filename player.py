import pygame
import random
import math

grid = 50

class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self,inx,iny,alpha):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create 50px by 50px surface
        self.image = pygame.Surface((50, 50))

        # color the surface cyan
        self.image.fill((0, 205, 205))
        self.rect = self.image.get_rect()
        self.image.set_alpha(alpha)
        self.snow_list = []

        # define self variables
        self.rect.x = inx
        self.rect.y = iny
        self.nx = self.rect.x
        self.ny = self.rect.y
        self.dx = self.rect.x
        self.dy = self.rect.y
        self.ox = self.rect.x
        self.oy = self.rect.y
        self.myspeed = 10
        self.inmotion = False
        self.dead = False

        # prepare the blood cannon
        self.blood = False

    def can_move(self):
        return (self.nx == self.rect.x) and (self.ny == self.rect.y) and not(dead)

    def left(self):
        if self.can_move:
            self.dx = self.rect.x - grid

    def right(self):
        if self.can_move:
            self.dx = self.rect.x + grid

    def up(self):
        if self.can_move:
            self.dy = self.rect.y - grid

    def down(self):
        if self.can_move:
            self.dy = self.rect.y + grid

    def move(self):
        if self.dead:
            self.image.set_alpha( self.image.get_alpha()/2.0 ) # fade out
            if not(self.blood):
                for i in range(500):
                    self.snow_list.append([[random.randrange(self.rect.x, self.rect.x+50),random.randrange(self.rect.y, self.rect.y+50)],[random.uniform(-2,2)**3,random.uniform(-2,2)**3],random.uniform(1, 3)])
                self.blood = True
            for i in range(500):
                self.snow_list[i][0][0] += self.snow_list[i][1][0]
                self.snow_list[i][0][1] += self.snow_list[i][1][1]
                self.snow_list[i][1][0] = self.snow_list[i][1][0]/1.1
                self.snow_list[i][1][1] = self.snow_list[i][1][1]/1.1


        if self.can_move:
            self.inmotion = False
            self.ox = self.rect.x
            self.oy = self.rect.y
        if (self.rect.x < self.nx):
            self.rect.x += self.myspeed
        if (self.rect.x > self.nx):
            self.rect.x -= self.myspeed
        if (self.rect.y < self.ny):
            self.rect.y += self.myspeed
        if (self.rect.y > self.ny):
            self.rect.y -= self.myspeed

        if (abs(self.rect.x - self.nx) < self.myspeed):
            self.rect.x = self.nx
        if (abs(self.rect.y - self.ny) < self.myspeed):
            self.rect.y = self.ny

    def keyboardhandler(self,key):
        if self.inmotion == False:
            if key == pygame.K_LEFT:
                self.left()
            elif key == pygame.K_RIGHT:
                self.right()
            elif key == pygame.K_UP:
                self.up()
            elif key == pygame.K_DOWN:
                self.down()
            self.inmotion = True
