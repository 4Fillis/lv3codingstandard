#Not following any tutorial, we go freelance
import pygame
import sys
import time

#color variables
bg_clr = (251, 247, 215)
plyr_clr = (254, 200, 216)

#main sprite variables
plyr_speed = 5
xpos = 100
ypos = 100
hght = 20
wdth = 20


#starting pygame
pygame.init()
#creating window
pygame.display.set_caption("hella sick game")
screen = pygame.display.set_mode((640, 480))
screen.fill(bg_clr)
#clock for making game run at 60fps to avoid crashes
clock = pygame.time.Clock()



rungame = True

while rungame == True:
    #if the user quits the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Checking for move key inputs
    press = pygame.key.get_pressed()
    if press[pygame.K_UP]: ypos-=plyr_speed
    if press[pygame.K_DOWN]: ypos+=plyr_speed
    if press[pygame.K_LEFT]: xpos-=plyr_speed
    if press[pygame.K_RIGHT]: xpos+=plyr_speed


    #drawing sprite
    screen.fill(bg_clr) # Clear screen with black
    pygame.draw.rect(screen, plyr_clr, (xpos, ypos, hght, wdth)) # Draw red square
    pygame.display.update()

    #fps to stop crashes
    clock.tick(60)