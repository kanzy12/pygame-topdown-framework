# Import a library of functions called 'pygame'
import pygame
import random
import math

class Blood(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self,inx,iny):

        WHITE = [200, 50, 0]

        # Loop 50 times and add a snow flake in a random x,y position
        for i in range(500):
            x = random.randrange(inx-25, inx+25)
            y = random.randrange(iny-25, iny+25)
            sx = random.uniform(-2,2)
            sx = math.copysign(sx**4,sx)
            sy = random.uniform(-2,2)
            sy = math.copysign(sy**4,sy)
            radius = random.uniform(1, 3)
            snow_list.append([[x,y],[sx,sy],radius])
