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
        #resizing cloud
        width = self.img.get_rect().width
        height = self.img.get_rect().height
        self.img = pygame.transform.scale(self.img, (width*0.6, height*0.6))

        #cloud starting position
        self.img_pos = [400, 200]
        #boolean for cloud movement, [upkey, downkey] <-- being held down
        self.movement = [False, False]
    def run(self):
        #infite loop
        while True:
            #clearing screen
            self.screen.fill((147, 47, 168))
            #cloud movement using boolean --=> integer trick, mult for speed change
            self.img_pos[1] += (self.movement[0] - self.movement[1]) 
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
                if event.type == pygame.KEYDOWN: #key pressed
                    print("key pressed")
                    if event.key == pygame.K_DOWN: #up key pressed
                        self.movement[0] = True  #up move = true
                        print("down key pressed")
                    if event.key == pygame.K_UP: #down key pressed
                        self.movement[1] == True#
                        self.img_pos[1] -= 10
                        print("up key pressed")
                if event.type == pygame.KEYUP: #key released
                    if event.key == pygame.K_UP: #up key released
                        self.movement[0] = False #stop moving up
                        print("up key released")
                    if event.key == pygame.K_DOWN: #down key released
                        self.movement[1] == True #
                        print("down key released")
            


            #function to keep screen on (otherwise goes black)
            pygame.display.update()
            #making game run at 60fps
            self.clock.tick(60)

#initialising game
Game().run()