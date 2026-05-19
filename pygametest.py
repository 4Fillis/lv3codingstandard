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
        #clock for making game run at 60fps to avoid crashes
        self.clock = pygame.time.Clock()
        clock = pygame.time.Clock()

        #loading cloud img, png files reccomended
        self.img = pygame.image.load('pygamerescources\images\cloud.png')

        #cloud starting position
        self.img_pos = [160, 260]
        #boolean for cloud movement, [upkey, downkey] <-- being held down
        self.movement = [False, False]
    def run(self):
        #infite loop
        while True:
            #cloud movement using boolean --=> integer trick
            self.img_pos[1] += self.movement[1] - self.movement[0]
            #using blit to add cloud to screen, top left is (0, 0)
            self.screen.blit(self.img, self.img_pos)

            #Events
            for event in pygame.event.get():
                #if user quits the window
                if event.type == pygame.QUIT:
                    #closes pygame and exits the system
                    pygame.quit()
                    sys.exit()
                #if user presses up/down keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] == True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] == False

            #function to keep screen on (otherwise goes black)
            pygame.display.update()
            #making game run at 60fps
            self.clock.tick(60)

#initialising game
Game().run()