#Not following any tutorial, we go freelance
import pygame
import sys
import time

#color variables
bg_clr = (251, 247, 215)
plyr_clr = (254, 200, 216)
#starting pygame
pygame.init()
#creating window
pygame.display.set_caption("hella sick game")
screen = pygame.display.set_mode((640, 480))
screen.fill(bg_clr)
#clock for making game run at 60fps to avoid crashes
clock = pygame.time.Clock()

#main sprite
plyr_speed = 5
x = 100
y = 100

rungame = True


while rungame == True:
    #if the user quits the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Checking for move key inputs
    press = pygame.key.get_pressed()
    if press[pygame.K_UP]: y-=plyr_speed
    if press[pygame.K_DOWN]: y+=plyr_speed
    if press[pygame.K_LEFT]: x-=plyr_speed
    if press[pygame.K_RIGHT]: x+=plyr_speed


    # 4. Redraw Everything
    screen.fill(bg_clr) # Clear screen with black
    pygame.draw.rect(screen, plyr_clr, (x, y, 20, 20)) # Draw red square
    pygame.display.update()
    # Control frame rate
    clock.tick(60)