import pygame
import math
import sys
import os
import UserString
from level import *
from menu import *
from player import *
from objects import *
import random

start_level = 1
grid = 50

class Controller(pygame.sprite.Sprite):
    def __init__(self, level_num):
        self.level = Level()
        level_string = "level" + str(level_num)
        #for testing
        #level_string = "leveltest"
        self.complete = False
        self.players = []
        self.playerpositions, self.time, self.switches, self.death_machines = self.level.load_file(level_string)
        self.playercount = len(self.playerpositions)

        for coordinate in self.playerpositions:
            self.players.append(Player(grid*coordinate[0],grid*coordinate[1],255/self.playercount))
            
        #add all objects to object_map
        self.object_map = {}
        for switch in self.switches:
            self.object_map[switch.position] = switch
        for death_machine in self.death_machines:
            self.object_map[death_machine.position] = death_machine

    def move_check(self,player):
        if (player.inmotion):
            if not(self.level.is_wall(player.dx/grid,player.dy/grid)):
                player.nx = player.dx
                player.ny = player.dy
                
                #check if stepped off something
                old_position = (player.ox/grid, player.oy/grid)
                if old_position in self.object_map:
                    cur_object = self.object_map[old_position]
                    
                    #it's a switch
                    if isinstance(cur_object, Switch):
                        cur_object.step_off()
                        if cur_object.toggle_changed:
                            self.switch_changed(cur_object, cur_object.targets)
                            cur_object.toggle_changed = False
                
                #check if it's goal
                if player.nx/grid == self.level.goal[0] and player.ny/grid == self.level.goal[1]:
                    self.complete = True
                else:
                    position = (player.nx/grid, player.ny/grid)
                    
                    #check if the position is an object
                    if position in self.object_map:
                        cur_object = self.object_map[position]
                        
                        #it's a switch
                        if isinstance(cur_object, Switch):
                            cur_object.step_on()
                            if cur_object.toggle_changed:
                                self.switch_changed(cur_object, cur_object.targets)
                                cur_object.toggle_changed = False
                        elif isinstance(cur_object, DeathMachine):
                            player.dead = True                
                            
            else:
                player.dx = player.rect.x
                player.dy = player.rect.y
            
    def switch_changed(self, switch, targets):
        if isinstance(switch, Switch):
            for target in targets:
                if self.level.map[target[1]][target[0]] == "#":
                    string = UserString.MutableString(self.level.map[target[1]])
                    string[target[0]] = "."
                    self.level.map[target[1]] = str(string)
                elif self.level.map[target[1]][target[0]] == ".":
                    string = UserString.MutableString(self.level.map[target[1]])
                    string[target[0]] = "#"
                    self.level.map[target[1]] = str(string)
                    for player in self.players:
                        if player.ox / grid == target[0] and player.oy / grid == target[1]:
                            print "Player Die!"
                            player.dead = True
        elif isinstance(switch, LaserSwitch):
            for target in targets:
                if switch.orientation == "vertical":
                    if self.level.map[target[1]][target[0]] == "I":
                        string = UserString.MutableString(self.level.map[target[1]])
                        string[target[0]] = "."
                        self.level.map[target[1]] = str(string)
                    else:
                        string = UserString.MutableString(self.level.map[target[1]])
                        string[target[0]] = "I"
                        self.level.map[target[1]] = str(string)
                elif switch.orientation == "horizontal":
                    if self.level.map[target[1]][target[0]] == "-":
                        string = UserString.MutableString(self.level.map[target[1]])
                        string[target[0]] = "."
                        self.level.map[target[1]] = str(string)
                    else:
                        string = UserString.MutableString(self.level.map[target[1]])
                        string[target[0]] = "-"
                        self.level.map[target[1]] = str(string)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        self.image = pygame.image.load(os.path.join('images', 'ball.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0

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
    current_level = start_level
    controller = Controller(current_level)

    # initialize the death counter
    deathcount = 0
    dt = 200
    deathoverlay = pygame.image.load(os.path.join('images', 'blood.png')).convert()
    WHITE = [200, 50, 0]
    s = pygame.Surface((650,500))
    s.set_colorkey([0,0,0])

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

            if not(player.dead):
                sprite_list.add(player)
            else:
                for item in player.snow_list:
                    pygame.draw.circle(s, WHITE, item[0], item[2])
        
        # if level is complete
        if controller.complete:
            screen.fill((0, 0, 0))
            s = pygame.Surface((650,500))
            s.set_colorkey([0,0,0])
            for player in controller.players:
                sprite_list.remove(player)
            current_level += 1
            controller = Controller(current_level)
            continue
        
        # black background
        screen.fill((0, 0, 0))
        background = controller.level.render()
        
        screen.blit(background,(0,0))    

        text = basicFont.render('#YOLO: %d' % math.ceil(controller.time), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.left = 4
        textRect.bottom = screen_rect.height

        # draw the player and enemy sprites to the screen
        s.set_alpha(200)
        screen.blit(s, (0,0))
        sprite_list.draw(screen)

        # display the timer on the bottom left
        if controller.time > 0:
            controller.time -= 0.02222222222
        else:
            controller.time = 0
            if dt > 1:
                dt -= 1
            else:
                dt = 0
            # draw the death overlay
            deathoverlay.set_alpha( abs(200-dt) )
            screen.blit(deathoverlay,(0,0))
            for player in controller.players:
                player.dead = True

        # draw the text onto the surface
        screen.blit(text, textRect)

        # draw the death overlay
        #screen.blit(deathoverlay, random.uniform(-1,1)*deathtransition, random.uniform(-1,1)*deathtransition)

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
    pygame.display.set_caption("YOU CLONELY LIVE ONCE")

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
                pygame.display.set_caption("YOU CLONELY LIVE ONCE: Expert Mode")
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
