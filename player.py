import pygame

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
        #self.image = pygame.image.load(os.path.join('images', 'ball.png'))
        self.rect = self.image.get_rect()
        self.image.set_alpha(alpha)
        #define self variables
        self.rect.x = inx
        self.rect.y = iny
        self.nx = self.rect.x
        self.ny = self.rect.y
        self.dx = self.rect.x
        self.dy = self.rect.y
        self.ox = self.rect.x
        self.oy = self.rect.y
        self.myspeed = 10
        self.moving = False

    def left(self):
        if (self.nx == self.rect.x) and (self.ny == self.rect.y):
            self.dx = self.rect.x - grid

    def right(self):
        if (self.nx == self.rect.x) and (self.ny == self.rect.y):
            self.dx = self.rect.x + grid

    def up(self):
        if (self.nx == self.rect.x) and (self.ny == self.rect.y):
            self.dy = self.rect.y - grid

    def down(self):
        if (self.nx == self.rect.x) and (self.ny == self.rect.y):
            self.dy = self.rect.y + grid

    def move(self):

        if (self.nx == self.rect.x) and (self.ny == self.rect.y):
            self.moving = False
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

#        if not((self.nx % self.grid) == 0):
#            self.nx = math.floor(self.nx/self.grid)*self.grid
#            self.rect.x = self.nx
#        if not((self.ny % self.grid) == 0):
#            self.ny = math.floor(self.ny/self.grid)*self.grid
#            self.rect.y = self.ny

    def keyboardhandler(self,key):
        if self.moving == False:
            if key == pygame.K_LEFT:
                self.left()
            elif key == pygame.K_RIGHT:
                self.right()
            elif key == pygame.K_UP:
                self.up()
            elif key == pygame.K_DOWN:
                self.down()
            self.moving = True
