#Following DaFluffyPotato's yt coding tutorial
import pygame
import sys

#making the game an object for OOP
class Game:
    def __init__(self):
        #Initialising pygame
        pygame.init()

        #window label
        pygame.display.set_caption("hella sick game")
        #creating window,      -      pixel resolution of the window
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        #loading cloud img, png files reccomended
        self.img = pygame.image.load('pygamerescources\images\cloud.png')


        #clock for making game run at 60fps to avoid overheating comptuter
        clock = pygame.time.Clock()
        #inputting an image
        #self.img = pygame.image.load('')
    def run(self):
        #infite loop
        while True:
            #adding cloud to screen
            self.screen.blit(self.img, (100, 200))
            #gets the input
            for event in pygame.event.get():
                #if user quits the window
                if event.type == pygame.QUIT:
                    #closes pygame and exits the system
                    pygame.quit()
                    sys.exit()

            #function to keep screen on (otherwise goes black)
            pygame.display.update()
            #making game run at 60fps
            self.clock.tick(60)

#initialising game
Game().run()