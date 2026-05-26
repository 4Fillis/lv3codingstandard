#Not following any tutorial, we go freelance
import pygame
import sys
import time

pygame.init()

#window label
pygame.display.set_caption("hella sick game")

#creating window,      -      pixel resolution of the window
screen = pygame.display.set_mode((640, 480))
#clock for making game run at 60fps to avoid crashes
clock = pygame.time.Clock()
rungame = True

while rungame == True:
    #if the user quits the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()