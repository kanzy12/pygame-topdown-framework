""" 
 Animating multiple objects using a list.
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/Gkhz3FuhGoI
"""
 
# Import a library of functions called 'pygame'
import pygame
import random
import math
 
# Initialize the game engine
pygame.init()
 
BLACK = [  0,   0,   0]
WHITE = [200, 50, 0]
 
# Set the height and width of the screen
SIZE = [400, 400]
 
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snow Animation")
 
# Create an empty array
snow_list = []
 
# Loop 50 times and add a snow flake in a random x,y position
s = pygame.Surface((1000,750))
for i in range(500):
    x = random.randrange(190, 210)
    y = random.randrange(190, 210)
    sx = random.uniform(-2,2)
    sx = math.copysign(sx**4,sx)
    sy = random.uniform(-2,2)
    sy = math.copysign(sy**4,sy)
    radius = random.uniform(1, 3)
    snow_list.append([[x,y],[sx,sy],radius])

clock = pygame.time.Clock()
 
#Loop until the user clicks the close button.
done = False
while done == False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Process each snow flake in the list
    for i in range(len(snow_list)):
     
        # Draw the snow flake
        pygame.draw.circle(screen, WHITE, snow_list[i][0], snow_list[i][2] )

         
        # Move the snow flake down one pixel
        snow_list[i][0][0] += snow_list[i][1][0]
        snow_list[i][0][1] += snow_list[i][1][1]
        snow_list[i][1][0] = snow_list[i][1][0]/1.1
        snow_list[i][1][1] = snow_list[i][1][1]/1.1

        if WHITE[1] > 0:
            WHITE[1] -= 0.05
        if WHITE[0] > 0:
            WHITE[0] -= 0.02
        else:
            snow_list = []
            WHITE = [255, 50, 0]
             
    # Go ahead and update the screen with what we've drawn.
    s.set_alpha(10)
    screen.blit(s, (0,0)) 
    pygame.display.flip()
    clock.tick(20)
             
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
