#Not following any tutorial, we go freelance
import pygame
from pygame.locals import *
import sys
from random import randint
from time import sleep

#SQL libraries import
import sqlite3

#color variables
bg_clr = (251, 247, 215)
plyr_clr = (160, 117, 230)
gnd_clr = (254, 200, 216)
lva_clr = (212, 50, 0)
wtr_clr = (15, 182, 212)

#main sprite variables
plyr_speed = 5
xpos = 100
ypos = 100
hght = 20
wdth = 20

#fancy pieces sprite variables
x_stonel = 50
y_stonel = 50

#opens db connection or creates one
conn = sqlite3.connect("objects.db")
#creating cursor
cursor = conn.cursor()
#creating databases for game use
rundb = False
if rundb:
    #silly data structures time
    cursor.executescript('''
    DROP TABLE IF EXISTS Room;
    DROP TABLE IF EXISTS Objects;
    CREATE TABLE Room(
    RoomID INTEGER NOT NULL,
    RoomName TEXT NOT NULL,
    PRIMARY KEY(RoomID)
    );

    INSERT INTO Room(RoomID, RoomName) VALUES
    (1,"Stairs"), 
    (2,"PC Room"), 
    (3,"Barn"),
    (4,"Kitchen");

    CREATE TABLE Objects(
    ObjectID NUMERIC NOT NULL,
    ObjectName NUMERIC NOT NULL,
    RoomID INTEGER,
    FOREIGN KEY(RoomID) REFERENCES Room(RoomID),
    PRIMARY KEY(ObjectID)
    );

    INSERT INTO Objects(ObjectID, ObjectName, RoomID) VALUES
    (15001,"Fluffy Rug",2),
    (15002,"Necklace",2),
    (15003, "Bed",2),
    (15004,"Table",4),
    (15005,"Waffles",4),
    (15006,"Clock",2),
    (15007,"Hay",NULL),
    (15008,"Hay",3),
    (15009,"Sink",4),
    (15010,"Water trough",3);

    ''')
    #getting objects in PC Room
    cursor.execute("SELECT * FROM Objects WHERE RoomID = 2")

    result = cursor.fetchall()
    for row in result:
        print(row)



#starting pygame
pygame.init()
#creating window
pygame.display.set_caption("hella sick game")
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(bg_clr)
#clock for making game run at 60fps to avoid crashes
clock = pygame.time.Clock()

#player character class
class Plyr:
    def __init__(self):
        #loading sprite img, png files reccomended
        self.img = pygame.image.load('pygamerescources\images\mc.png')
        #resizing sprite
        scale = 0.3
        n_width = int((self.img.get_rect().width)*scale)
        n_height = int((self.img.get_rect().height)*scale)
        self.img = pygame.transform.scale(self.img, (n_width, n_height))
        self.xpos = 30
        self.ypos = 0 
        #self.rect = pygame.Rect(self.xpos, self.ypos, n_width, n_height)

#creating the player sprite object
plyr = Plyr()

#special stones class
class Treasure:
    def __init__(self):
        #loading sprite img, png files reccomended
        self.img = pygame.image.load('pygamerescources\images\duck.webp')
        self.hb = self.img.get_rect()
        #resizing sprite
        width = self.img.get_rect().width
        height = self.img.get_rect().height
        self.img = pygame.transform.scale(self.img, (int(width*0.2), int(height*0.2)))

        self.xpos = 50
        self.ypos = 50 

#player character class
class Platform:
    def __init__(self):

        self.xpos = randint(0, 500)
        self.ypos = randint(0, 500) 
        self.pos = [self.xpos, self.ypos]


#Rock pos dict for collision checking
rocks_pos = {
    "lwrypos" : [],
    "lwrxpos" : [],
    
    "uprypos" : [],
    "uprxpos" : [],

    "airypos" : [],
    "airxpos" : [],
}

#platform arrangement dict, 
#start coords are 1st list item, start type & % of screen width is the 2nd list item
createrocks = {
    "lwr": [[1, 400], ["gnd", 1, 2, 3, 4, 5]],
    "upr": [[1, 100], ["gnd", 1, 1, 1, 1]],
    "air": [[1, 250], ["air", 1, 2, 3, 4, 5]]
}


#dict for attributes of gnd types
#rendered y/n, color
gndtypes = {
    "air": [False, "no"],
    "gnd": [True, gnd_clr],
    "lava": [True, lva_clr],
    "water": [True, wtr_clr]
}


rocks = []
def draw_lvl(rocks):
    #variables/lists needed
    platwidth = 0
    xpos = 0
    #for each height of platforms specified in the lvl
    for key in createrocks:
        #finding the total amt of platforms
        #avoiding empty errors by turning empty lvls into just air
        if not createrocks[key]:
            createrocks[key] = [[0, 0], ["air", 1]]
        platforms = createrocks[key][1]
        if platforms[0] == "air":
            platforms.insert(1, 0)
        print("platofrms 0")
        print(platforms[0])
        #finding how long each platform is
        #each levels y position
        ypos = createrocks[key][0][1]
        for x in range(1):
            xpos += createrocks[key][0][0] 
            #totalpcent is the same as platforms without the starttype
            totalpcent = createrocks[key][1]
            print("platofrms 1")
            print(platforms[0])
            totalpcent.pop(0)
                
            print("platforms/totalpcent 1")
            print(platforms[0])
            print(totalpcent)
            platx = int(screen_width/sum(totalpcent))
            
            platforms = createrocks[key][1]
            print("platforms/totalpcent 2")
            print(platforms[0])
            print(totalpcent)

            #if the lvl starts with air:
            #skip platform generation and move the cursor the platform width over
            print(f"platforms  b4 air check {[platforms]}")
            print(platforms[0])

            #listing air/ground ratios
            rendergnds = platforms[::2]
            #remove the start type so every 2nd one is air
            platforms.pop(0)
            renderair = platforms[::2]

            #for the amt of platforms, generate a gnd then air slab
            for i in range(len(renderair)+len(rendergnds)):
                #creating slab section if it should exist
                if len(rendergnds) > 0:
                    print(f"rendergnds2 {rendergnds}")
                    platwidth = platx*rendergnds[0]
                    rock = Platform()
                    rock_rect = pygame.Rect(xpos, ypos, platwidth, 50)
                    rocks.append(rock_rect)
                    rendergnds.pop(0)
                if len(renderair) > 0:
                    #'generating' the air slab
                    xpos += platwidth + platx*renderair[0]
                    renderair.pop(0)
        #resetting xpos to LHS of screen
        xpos = 0
    return(rocks)

draw_lvl(rocks)
#game loop
rungame = True
while rungame == True:
    #if the user quits the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #checking for collisions
    plyr_rect = pygame.Rect(plyr.xpos, plyr.ypos, 50, 50)
    for rock in rocks:
        if plyr_rect.colliderect(rock):
            #topcheck
            print(rock.top)
            print(f"rock {rock}")
            if plyr_rect.bottom >= rock.top:
                print("quack\nquack\n")

    #checking for move key inputs
    press = pygame.key.get_pressed()
    if press[pygame.K_UP]: plyr.ypos-=plyr_speed
    if (press[pygame.K_DOWN]): 
        plyr.ypos+=plyr_speed
    if press[pygame.K_LEFT]: plyr.xpos-=plyr_speed
    if press[pygame.K_RIGHT]: plyr.xpos+=plyr_speed

    #clearing screen
    screen.fill(bg_clr)
    #using blit to add sprites to screen, top left is (0, 0)
    screen.blit(plyr.img, (plyr.xpos, plyr.ypos))
    for rock in rocks:
        pygame.draw.rect(screen, plyr_clr, rock)

    
    pygame.display.update()

    #fps to stop crashes
    clock.tick(60)
