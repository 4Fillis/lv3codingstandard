#Following DaFluffyPotato's yt coding tutorial
import pygame
import sys
import time

#making the game an object for OOP
class Game:
    def __init__(self):
        #Initialising pygame
        pygame.init()

        #window label
        pygame.display.set_caption("hella sick game")
        #creating window,      -      pixel resolution of the window
        self.screen = pygame.display.set_mode((640, 480))
        #clock for making game run at 60fps to avoid crashes
        self.clock = pygame.time.Clock()
        clock = pygame.time.Clock()

        #loading sprite img, png files reccomended
        self.img = pygame.image.load('pygamerescources\images\hannah.png')
        #resizing sprite
        width = self.img.get_rect().width
        height = self.img.get_rect().height
        self.img = pygame.transform.scale(self.img, (width*0.6, height*0.6))

        #sprite starting position
        self.img_pos = [400, 200]
    def run(self):
        #movement speed
        move = 5
        while True:
            #clearing screen
            self.screen.fill((147, 47, 168))
            #using blit to add sprite to screen, top left is (0, 0)
            self.screen.blit(self.img, self.img_pos)
            #Events
            for event in pygame.event.get():
                #if user quits the window
                if event.type == pygame.QUIT:
                    #closes pygame and exits the system
                    pygame.quit()
                    sys.exit()
                #User movement Version 2.0
            x = 0
            y = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:  x -= move
            if keys[pygame.K_RIGHT]: x += move
            if keys[pygame.K_UP]:    y -= move
            if keys[pygame.K_DOWN]:  y += move
            self.img_pos[0] += x
            self.img_pos[1] += y
            #using blit to add sprite to screen, top left is (0, 0)
            self.screen.blit(self.img, self.img_pos)
            #keep screen on (otherwise goes black)
            pygame.display.update()
            #making game run at 60fps
            self.clock.tick(60)

#initialising game
Game().run()