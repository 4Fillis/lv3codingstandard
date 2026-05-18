#Following DaFluffyPotato's yt coding tutorial
import pygame
import sys

#Initialising pygame
pygame.init()

#creating window,      -      pixel resolution of the window
screen = pygame.display.set_mode(640, 480)

#clock for making game run at 60fps to avoid overheating comptuter
clock = pygame.time.clock()

#infinit loop
while True:
    #gets the input
    for event in pygame.event.get():
        #if user quits the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit

    #function to keep screen on (otherwise goes black)
    pygame.display.update()
    #making game run at 60fps
    clock.tick(60)