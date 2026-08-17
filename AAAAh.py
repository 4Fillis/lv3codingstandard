#Dictionaries to import
import pygame
from pygame.locals import *
import sys
from random import randint
from time import sleep
import os
from collections import defaultdict

#SQL libraries import
import sqlite3

#color variables

plyr_clr = (22, 164, 235)
bg_clr = (158, 233, 255)
gnd_clr = (24, 82, 38)
lva_clr = (163, 61, 29)
wtr_clr = (38, 159, 181)

print(f"clrs, gnd={gnd_clr}, wtr={wtr_clr}, lva={lva_clr}")
#main sprite variables
plyr_speed = 3
dy = 0.0
grav = 0.6
max_speed = 10
#negitive bcos y distance is distance from top
jump_speed = -5
xpos = 100
ypos = 100
yresetpoint = 30
xresetpoint = 30
plyr_width = 40
plyr_height = 40

platheight = 50

#fancy pieces sprite variables
x_stonel = 50
y_stonel = 50


#achievements, defaults to false
achievements = {
    #how many stones found
    "stones": [0, 0, 0, 0, 0],
    "deaths": 0,
    #completed the whole thing without dying
    "one life": False,
    #completed the game
    "awakened": False,
    "speedrunner": False,
    "the ultimate speedrunner": False,
    #talked to all the NPCS in the game
    "chatty": [0, 0, 0, 0, 0]
}
#file for achievement storage
#file name
file_path = "file.txt"
#opening the file in read and write mode or creating it if it exists
#non-+ write mode won't let you edit the data
f = open(file_path, "w+")


    
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
screen_width = 750
screen_height = 550
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
class Portal:
    def __init__(self):
        #loading sprite img, png files reccomended
        self.img = pygame.image.load('pygamerescources\images\nether_portal.png')
        self.hb = self.img.get_rect()
        #resizing sprite
        width = self.img.get_rect().width
        height = self.img.get_rect().height
        self.img = pygame.transform.scale(self.img, (int(width*0.2), int(height*0.2)))

        self.xpos = 250
        self.ypos = 400

#platform superclass
class Platform:
    def __init__(self, solid: bool, sped_efct: float, grav_efct: float, clr: str, 
                xcoord: int, ycoord: int, width: int, height: int):
        #setting attributes
        self.solid = solid
        self.sped_efct = sped_efct
        self.grav_efct = grav_efct
        self.clr = clr
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.xcoord, self.ycoord, self.width, self.height)

#Subclasses for different platform types
class Gnd(Platform):
    def __init__(self, solid = True, sped_efct = 0.0, grav_efct = 0.0, clr = gnd_clr, xcoord = 0, ycoord = 0, width = 100, height = platheight) -> None:
        super().__init__(solid=solid, sped_efct=sped_efct, grav_efct=grav_efct, clr = clr,
                        xcoord=xcoord, ycoord=ycoord, width=width, height=height)


class Lva(Platform):
    def __init__(self, solid = False, sped_efct = 0.8, grav_efct = 0.5, clr = lva_clr, xcoord = 0, ycoord = 0, width = 100, height = platheight) -> None:
        super().__init__(solid=solid, sped_efct=sped_efct, grav_efct=grav_efct, clr = clr,
                        xcoord=xcoord, ycoord=ycoord, width=width, height=height)


class Wtr(Platform):
    def __init__(self, solid = False, sped_efct = 0.8, grav_efct = 0.5, clr = wtr_clr, xcoord = 0, ycoord = 0, width = 100, height = platheight) -> None:
        super().__init__(solid=solid, sped_efct=sped_efct, grav_efct=grav_efct, clr = clr,
                        xcoord=xcoord, ycoord=ycoord, width=width, height=height)


platcodes = {
    #101 = Air not included in this because it isnt a subclass as it has no needed properties
    102: Gnd,
    103: Lva,
    104: Wtr
}
#starting on level 1
lvl = 1

game_platforms = {
    #1,2,3 is the level number, startcoords is where the lvl starts in the screen (x, y)
    #defaulttype is the default platform type to prevent having to always specify the type
    #formation [a, b] form, a is the platform type, b is what % of the screen it is
    #% is done with the sum of all the level platforms (ex. 2 + 4 + 1 = 7, 2/7 = 2/7th of the screen for that platform)
    1: {"upr": {
            #y coord is distance from top
            "startcoords": [0, 120],
            "defaulttype": 102,
            "formation": [[102, 1], [101, 4], [102, 2]]},
        "air": {
            "startcoords": [0, 250],
            "defaulttype": 102,
            "formation": [[102, 2], [101, 3], [103, 1]]},
        "lwr": {
            "startcoords": [0, 400],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 2]]}},
    
    2: {"upr": {
            "startcoords": [0, 50],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "air": {
            "startcoords": [0, 10],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "lwr": {
            "startcoords": [0, 300],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]}},
    3: {"upr": {
            "startcoords": [0, 100],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "air": {
            "startcoords": [0, 200],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "lwr": {
            "startcoords": [0, 300],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]}},
    4: {"upr": {
            "startcoords": [0, 50],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "air": {
            "startcoords": [0, 250],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "lwr": {
            "startcoords": [0, 450],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]}},
    5: {"upr": {
            "startcoords": [0, 320],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "air": {
            "startcoords": [0, 20],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]},
        "lwr": {
            "startcoords": [0, 100],
            "defaulttype": 102,
            "formation": [[102, 2], [102, 1], [103, 1]]}},
}

#reset function
def check_alive():
    if plyr.ypos > (screen_height+100):
        plyr.xpos = 30
        plyr.ypos = 30
    return(plyr.xpos, plyr.ypos)


#function note: "%" is the proportion of the screen the platforms takes up 
# with the whole being the sum of all the level platform widths
plats = []
def draw_lvl(lvl, plats):
    print(f"lvl: {lvl}")
    #deleting last level platforms from list
    while len(plats) > 0:
        plats.pop(0)
    loops = 0
    #variables/lists needed
    platwidth = 0
    xpos = 0
    
    #to get all the level data from the dict w/o risking modifying the original
    createplats = game_platforms[lvl].copy()

    #for each lvl of platform
    for key in createplats:
        loops+=1
        #finding the total amt of platforms
        #avoiding empty errors by turning empty levels into just air
        if (not createplats[key]) or (len(createplats[key]) <= 1): 
            createplats[key] = {"startcoords": [1, 100], 
                                "defaulttype": 101, 
                                "formation": [1, 1]}

        #finding how long each platform is
        #each levels y position
        ypos = createplats[key]["startcoords"][1]

        #moving to start position if the lvl has one
        xpos = createplats[key]["startcoords"][0]

        #how long each platform is
        platlist = []
        #corresponding list of each platform type
        plattypes = []

        #creating a list of the types of platforms in Left->Right order
        #clearing list for a clean loop
        plattypes.clear()
        platlist.clear()
        for i in range(len(createplats[key]["formation"])):
            #checking if the platform has a specified type
            if type(createplats[key]["formation"][i]) == list:
                plattypes.append(createplats[key]["formation"][i][0])
                platlist.append(createplats[key]["formation"][i][1])
            else:
                plattypes.append(createplats[key]["defaulttype"])
                platlist.append(createplats[key]["formation"][i])

        print(f"Row: {key}")
        print(f"  plattypes: {plattypes}")
        print(f"  platlist: {platlist}")
        #skip if the lvl has no platforms
        if not platlist:
            continue

        #totalpcent is the % of all the platforms in that level added up
        totalpcent = sum(platlist)
        #setting each platwidth to its specified proportion
        platx = round((screen_width/totalpcent), 1)
        platx = int(platx)

        for i in range(len(platlist)):
            #platwidth is the platform length
            platwidth = platx*platlist[0]
                
            #creating the platform and then deleting it from the list
                
            #creating the platform in its type
            #checking and skipping air 'platforms'
            if plattypes[0] != 101:
                #creating the subclass instance & making it a platform
                plat = platcodes[plattypes[0]](xcoord=xpos, ycoord=ypos, width=platwidth, height=platheight)
                plats.append(plat)
                print(f"  → Class: {plat.__class__.__name__}, Color: {plat.clr}")
            #move to the next platform start point
            xpos += platwidth
            plattypes.pop(0)
            platlist.pop(0)
                
        #resetting xpos to LHS of screen
        xpos = 0
    #print(f"loops of key = {loops}")
    return(plats)

#find the next level
def next_lvl(lvl):
    lvl+=1
    draw_lvl(lvl, plats)
    #reset player location
    plyr.ypos = yresetpoint
    plyr.xpos = xresetpoint
    return(lvl)

draw_lvl(lvl, plats)
#game loop
rungame = True
on_gnd = False
#0 is if ignoring gnd for jump purposes, 1 is frame counter, 2 is frames to ignore it for
ignore_gnd = [False, 0, 40]
while rungame == True:
    #loop variables
    dy = 0.0
    on_gnd = False
    
    #if the user quits the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    #plyr rect for collisions
    plyr_rect = pygame.Rect(plyr.xpos, plyr.ypos, plyr_width, plyr_height)
    #checking for move key inputs
    press = pygame.key.get_pressed()
    #x change (left and right movement)
    dx = 0
    if (press[pygame.K_LEFT]):
        dx = -plyr_speed
    if (press[pygame.K_RIGHT]):
        dx = plyr_speed

    #rendering movement
    plyr.xpos += dx
    plyr_rect = pygame.Rect(plyr.xpos, plyr.ypos, plyr_width, plyr_height)

    #y change (up and down movement)
    dy = 0
    if on_gnd:
        #positive bcos distance is distance from top of screen
        dy = plyr_speed

    #jumping
    if press[pygame.K_UP] and (not on_gnd) and (not ignore_gnd[0]):
        ignore_gnd[0] = True
        ignore_gnd[1] = 0
        on_gnd = False
        dy = -plyr_speed

    #changing plyr coord
    plyr.xpos += dx
    plyr.ypos += dy

    #checking each plat for collisions
    #left and right
    for plat in plats:
        if plyr_rect.colliderect(plat.rect):
            #if moving right, player position set to avoid vibrating collision problem
            if dx > 0:
                plyr.xpos = plat.rect.left - plyr_width
            #if left
            elif dx < 0:
                plyr.xpos = plat.rect.right
            #if on_gnd :(
            elif dy > 0:
                plyr.ypos = plat.rect.top - plyr_height
                on_gnd = False
                #reset ignore_gnd
                ignore_gnd[0] = False
                ignore_gnd[1] = 0
            #if hitting btm of platform
            elif dy < 0:
                plyr.ypos = plat.rect.bottom
                #stop moving up
                dy = 0



    #clearing screen
    screen.fill(bg_clr)
    #using blit to add sprites to screen, top left is (0, 0)
    screen.blit(plyr.img, (plyr.xpos, plyr.ypos))
    for plat in plats:
        pygame.draw.rect(screen, plat.clr, plat.rect)
    
    check_alive(plyr.xpos, plyr.ypos)
    #resetting player to start if they go off the edge
    if (plyr.xpos > 610) and (plyr.ypos < 400):
        lvl = next_lvl(lvl)
    #print(f"plyr coords: [{plyr.xpos}, {plyr.ypos}]")
    #print(f"lvl: {lvl}")
    #print(f"[{plyr.xpos, plyr.ypos}]")
    #updating the display
    pygame.display.update()
    #fps to stop crashes
    clock.tick(60)
    