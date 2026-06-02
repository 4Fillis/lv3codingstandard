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

#fancy pieces sprite variables
x_stonel = 50
y_stonel = 50

#starting pygame
pygame.init()
#creating window
pygame.display.set_caption("hella sick game")
screen = pygame.display.set_mode((640, 480))
screen.fill(bg_clr)
#clock for making game run at 60fps to avoid crashes
clock = pygame.time.Clock()

#player character class
class Plyr:
    def __init__(self):
        #loading sprite img, png files reccomended
        self.img = pygame.image.load('pygamerescources\images\mc.png')
        #resizing sprite
        width = self.img.get_rect().width
        height = self.img.get_rect().height
        self.img = pygame.transform.scale(self.img, (int(width*0.4), int(height*0.4)))

        self.xpos = 100
        self.ypos = 100 

#creating the player sprite object
plyr = Plyr()


#infinite loop
rungame = True
while rungame == True:
    #if the user quits the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #checking for move key inputs
    press = pygame.key.get_pressed()
    if press[pygame.K_UP]: plyr.ypos-=plyr_speed
    if press[pygame.K_DOWN]: plyr.ypos+=plyr_speed
    if press[pygame.K_LEFT]: plyr.xpos-=plyr_speed
    if press[pygame.K_RIGHT]: plyr.xpos+=plyr_speed

    #clearing screen
    screen.fill(bg_clr)
    #using blit to add sprite to screen, top left is (0, 0)
    screen.blit(plyr.img, (plyr.xpos, plyr.ypos))

    pygame.draw.rect(screen, (0, 0, 0), (x_stonel, y_stonel, hght, wdth))
    
    
    pygame.display.update()

    #fps to stop crashes
    clock.tick(60)