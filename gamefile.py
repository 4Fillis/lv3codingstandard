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

#opens db connection or creates one
conn = sqlite3.connect("objects.db")
#creating cursor
cursor = conn.cursor()
#creating databases for game use
if True:
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
        scale = 0.3
        n_width = int((self.img.get_rect().width)*scale)
        n_height = int((self.img.get_rect().height)*scale)
        self.img = pygame.transform.scale(self.img, (n_width, n_height))
        self.hitbox = (n_width, n_height)
        self.xpos = 100
        self.ypos = 100 

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

#creating the rocks sprite object
rocks = []
for i in range(4):
    rock = Platform()
    rock_rect = pygame.Rect(rock.xpos, rock.ypos, 100, 100)
    rocks.append(rock_rect)
    rockypos = [rock.ypos]

#infinite loop
rungame = False
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
            print("quack\nquack\n")
            if plyr.ypos > (int(rockypos[0])+25):
                print("ypos")
                plyr.ypos-=plyr_speed
                sleep(0.1)

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
