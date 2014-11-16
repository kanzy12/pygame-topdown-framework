import pygame
import math
import sys
import os
import random
from level import *
from menu import *
from player import *

grid = 50
BLOOD = [200, 50, 0]

class Controller(pygame.sprite.Sprite):
    def __init__(self, level_num):
        self.level = Level()
        level_string = "level" + str(level_num) + ".map"
        self.complete = False
        self.players = []
        self.playerpositions, self.time = self.level.load_file(level_string)
        self.playercount = len(self.playerpositions)

        for coordinate in self.playerpositions:
            self.players.append(Player(grid*coordinate[0],grid*coordinate[1],255/self.playercount))
            
        print self.level.goal

    def move_check(self,player):
        if not(self.level.is_wall(player.dx/grid,player.dy/grid)):
            player.nx = player.dx
            player.ny = player.dy
            
            #check if it's goal
            if player.nx/grid == self.level.goal[0] and player.ny/grid == self.level.goal[1]:
                self.complete = True
        else:
            player.dx = player.rect.x
            player.dy = player.rect.y

class Switch(pygame.sprite.Sprite):
    def __init__(self):
        self.occupied = False
        self.toggle = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        self.image = pygame.image.load(os.path.join('images', 'ball.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0

class Wall(pygame.sprite.Sprite):
    def __init__(self,inx,iny):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # create 50px by 50px surface
        self.image = pygame.Surface((50, 50))
        # color the surface cyan
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        #define self variables
        self.rect.x = inx;
        self.rect.y = iny;

def event_loop():
    # get the pygame screen and create some local vars
    screen = pygame.display.get_surface()
    screen_rect = screen.get_rect()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    # set up font
    basicFont = pygame.font.SysFont(None, 48)
    # initialize a clock
    clock = pygame.time.Clock()

    #initialize the level
    current_level = 1
    controller = Controller(1)

    # initialize the death counter
    deathcount = 0
    deathtransition = 255
    deathoverlay = pyagme.Surface((650, 500))

    # create a sprite group for the player and enemy
    # so we can draw to the screen
    sprite_list = pygame.sprite.Group()
    for player in controller.players:
        sprite_list.add(player)

    # main game loop
    while 1:

        # handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                for player in controller.players:
                    player.keyboardhandler(event.key)

        # take keyboard inputs and check where players can move
        for player in controller.players:
            controller.move_check(player)
            player.move()
        
        # if level is complete
        if controller.complete:
            for player in controller.players:
                sprite_list.remove(player)
            current_level += 1
            controller = Controller(current_level)
            for player in controller.players:
                if not(player.dead):
                    sprite_list.add(player)              
            continue
        
        # black background
        screen.fill((0, 0, 0))
        background = controller.level.render()
        screen.blit(background,(0,0))    

        # display the timer on the bottom left
        if controller.time > 0:
            controller.time -= 0.02222222222
        else:
            controller.time = 0
            if deathtransition > 0:
                deathtransition -= 1
            for player in controller.players:
                player.dead = True

        text = basicFont.render('#YOLO: %d' % math.ceil(controller.time), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.left = 4
        textRect.bottom = screen_rect.height
        
        # draw the text onto the surface
        screen.blit(text, textRect)

        # draw the death overlay
        screen.blit(deathoverlay, random.uniform(-1,1)*deathtransition, random.uniform(-1,1)*deathtransition)

        # draw the player and enemy sprites to the screen
        sprite_list.draw(screen)

        # update the screen
        pygame.display.flip()

        # limit to 45 FPS
        clock.tick(45)

def main():
    # initialize pygame
    pygame.init()

    # create the window
    size = width, height = 650, 500
    screen = pygame.display.set_mode(size)

    # set the window title
    pygame.display.set_caption("Example Framework")

    # create the menu
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                 [('Start Game',   1, None),
                  ('Other Option', 2, None),
                  ('Exit',         3, None)])
    # center the menu
    menu.set_center(True, True)
    menu.set_alignment('center', 'center')

    # state variables for the finite state machine menu
    state = 0
    prev_state = 1

    # ignore mouse and only update certain rects for efficiency
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    rect_list = []

    while 1:
        # check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        # get the next event
        e = pygame.event.wait()

        # update the menu
        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
            if state == 0:
                # "default" state
                rect_list, state = menu.update(e, state)
            elif state == 1:
                # start the game
                event_loop()
            elif state == 2:
                # just to demonstrate how to make other options
                pygame.display.set_caption("y u touch this")
                state = 0
            else:
                # exit the game and program
                pygame.quit()
                sys.exit()

            # quit if the user closes the window
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # update the screen
            pygame.display.update(rect_list)

if __name__ == '__main__':
    main()
