import sys
import pygame
import sqlite3
import maps
from utils import load_image
import configuration as C
import numpy as np
import time
database = "./maps.db"
conn = sqlite3.connect(database)
sqlCreate = """CREATE TABLE IF NOT EXISTS levels (
                id integer PRIMARY KEY,
                mapID interger NOT NULL,
                levelData blob NOT NULL,
                north integer NOT NULL,
                east integer NOT NULL,
                south integer NOT NULL,
                west integer NOT NULL,
                 UNIQUE (mapID)
                );"""
cur = conn.cursor()
cur.execute(sqlCreate)
sqlCreate = """CREATE TABLE IF NOT EXISTS nodeGraphs (
                id integer PRIMARY KEY,
                mapID interger NOT NULL,
                nodeGraph blob NOT NULL,
                UNIQUE (mapID)
                );"""
cur = conn.cursor()
cur.execute(sqlCreate)
pygame.init()

WATER_IMAGE = load_image('water.png', 25, 25)
DIRT_IMAGE = load_image('dirt.png', 25, 25)
GRASS_IMAGE = load_image('grass.png', 25, 25)
STONE_IMAGE = load_image('stone.png', 25, 25)
TILEFLOOR_IMAGE = load_image('tilefloor.png',25,25)
ROCKYGROUND_IMAGE = load_image('rockyground.png',25,25)
NOTEXTURE_IMAGE = load_image('notexture.png',25,25)
screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
pygame.display.set_caption("map_editor")
basicfont = pygame.font.Font('assets/open24.ttf',20)
pygame.mouse.set_visible(False)
all_walls = pygame.sprite.Group()
all_cursors = pygame.sprite.Group()
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)
DARKRED = (128,0,0)
GREEN = (0,255,0)
BROWN = (128,64,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
gridSize = 25

        
class wall(pygame.sprite.Sprite):
    def __init__(self,tileposx,tileposy,tileType):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([gridSize,gridSize])
        self.tileType = tileType
        if self.tileType == 1:
            self.image = STONE_IMAGE
        elif self.tileType == 2:
            self.image = GRASS_IMAGE
        elif self.tileType == 3:
            self.image = DIRT_IMAGE
        elif self.tileType == 4:
            self.image = TILEFLOOR_IMAGE
        elif self.tileType == 5:
            self.image = ROCKYGROUND_IMAGE
        elif self.tileType == 6:
            self.image = WATER_IMAGE
        else:
            self.image.fill(RED)
        self.x = tileposx
        self.y = tileposy
        
        self.rect = pygame.Rect([self.x,self.y,gridSize,gridSize])
        all_walls.add(self)

def roundCoords(x,y):
    x = round(x/gridSize)*gridSize
    y = round(y/gridSize)*gridSize
    return(x,y)

def makeGrid(surface, width, height, spacing):
    for x in range(0, width, spacing):
        pygame.draw.line(surface, WHITE, (x,0), (x, height))
    for y in range(0, height, spacing):
        pygame.draw.line(surface, WHITE, (0,y), (width, y))
        
def snapToGrid(mousePos):
    if 0 < mousePos[0] < C.SCREEN_WIDTH and 0 < mousePos[1] < C.SCREEN_HEIGHT:
        return roundCoords(mousePos[0],mousePos[1])

def fillNewMap():
    #print("filling blank map with grass")
    x = 0
    while x < 976:
        y = 0
        while y < 701:
            pos = (x, y)
            all_walls.add(wall(x,y,2))
            y = y + gridSize
        x = x + gridSize

def getGroup():
#todo: read x/y coordinates from database
#todo: link each record in DB to others for nextmap
#todo: link player boundary with nextmap
    #wall(150,150)
    return(all_walls)

def clearArray(arrayToClear):
    for index in range(len(arrayToClear)):
        del arrayToClear[0]
        

mapID = 1
getGroup()
color = (128,128,128)
clock = pygame.time.Clock()
conn = sqlite3.connect(database)
cur = conn.cursor()
levelData = maps.loadMap(mapID)
tileType = 1
pos = pygame.mouse.get_pos()
mouse_x = pos[0]
mouse_y = pos[1]
snap_coord = snapToGrid(pos)
if snap_coord != None:
    mouse_x = snap_coord[0] + 10
    mouse_y = snap_coord[1] + 10


if len(levelData) < 1 :
    fillNewMap()
    
for item in levelData:
    x = item[0]
    y = item[1]
    tileType = item[2]
    all_walls.add(wall(x,y,tileType))

aiWalls = []
aiNodes = []
aiWallNodes = []
xNodes = []
while True:
    events = pygame.event.get()
    north = mapID  + 1
    east = mapID + 1000
    south = mapID - 1
    west = mapID - 1000
    for event in events:
        if event.type == pygame.KEYUP:
            #print(event.key)
            if event.key == 119:
                mapID = mapID + 1
                for item in all_walls:
                    item.kill()
                levelData = maps.loadMap(mapID)
                if len(levelData) < 1 :
                    fillNewMap()
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    color = item[2]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y,color))
            if event.key == 100:
                mapID = mapID + 1000
                for item in all_walls:
                    item.kill()
                levelData = maps.loadMap(mapID)
                if len(levelData) < 1 :
                    fillNewMap()
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    color = item[2]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y,color))
            if event.key == 115:
                mapID = mapID - 1
                for item in all_walls:
                    item.kill()
                levelData = maps.loadMap(mapID)
                if len(levelData) < 1 :
                    fillNewMap()
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    color = item[2]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y,color))
            if event.key == 97:
                mapID = mapID - 1000
                for item in all_walls:
                    item.kill()
                levelData = maps.loadMap(mapID)
                if len(levelData) < 1 :
                    fillNewMap()
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    color = item[2]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y,color))
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            snap_coord = snapToGrid(pos)
            if snap_coord != None:
                mouse_x = snap_coord[0] + 10
                mouse_y = snap_coord[1] + 10
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(str(event.button) + " DOWN")
            if event.button == 1:
                wall(snap_coord[0],snap_coord[1],tileType)
                print(str(snap_coord[0]) + ", " + str(snap_coord[1]))
            if event.button == 3:
                for item in all_walls:
                    if item.x == snap_coord[0] and item.y == snap_coord[1]:
                        item.kill()
            if event.button == 4:
                tileType = tileType - 1
            if event.button == 5:
                tileType = tileType + 1
            if tileType > 6:
                tileType = 1
            if tileType < 1:
                tileType = 6
            if event.button == 2:
                levelData = ""

                print("building nodegraph")
                for item in all_walls:
                    if item.tileType == 1:
                        x = int(item.x)
                        y = int(item.y)
                        aiWalls.append((x,y))
                    #print(aiWalls)
                    levelData = levelData + (str(item.x) + "," + str(item.y) + "," + str(item.tileType) + "|")
                    conn = sqlite3.connect(database)
                    cur = conn.cursor()
                print("wall objects identified")
                try:
                    sqlInsert = "INSERT INTO levels (levelData,mapID,north,east,south,west) VALUES ('" + str(levelData) + "'," + str(mapID) + "," + str(north) + "," + str(east) + "," + str(south) + "," + str(west) + ");"
                    cur.execute(sqlInsert)
                    print("level data written to db")
                except:
                    sqlInsert = "UPDATE levels SET levelData = '" + str(levelData) + "' WHERE mapID = " + str(mapID) + ";"
                    cur.execute(sqlInsert)
                    print("level data updated in db")
                conn.commit()
                print("compiling nodegraph from wall objects")
                #print(aiWalls)
                wallTable = ""
                tileX = 0
                tileY = 0
                row = ""
                tableSizeX = C.SCREEN_WIDTH
                tableSizeY = C.SCREEN_HEIGHT
                while tileY < tableSizeY:
                    tileX = 0
                    while tileX < tableSizeX:
                        pos = (tileX,tileY)
                        for node in aiWalls:
                            if node[0] == pos[0] and node[1] == pos[1]:
                                print("wall found @ " + str(pos))
                                row += "0,"
                                break
                        else:
                            row = row + "1,"
                        tileX = tileX + 25
                    tileY = tileY + 25
                    row = row + "|"
                    wallTable = wallTable + row 
                    row = ""
                
                try:
                    sqlInsert = "INSERT INTO nodeGraphs (nodeGraph,mapID) VALUES ('" + str(wallTable) + "'," + str(mapID) + ");"
                    cur.execute(sqlInsert)
                    print("nodegraph data written to db")
                except:
                    sqlInsert = "UPDATE nodeGraphs SET nodeGraph = '" + str(wallTable) + "' WHERE mapID = " + str(mapID) + ";"
                    #print(sqlInsert)
                    cur.execute(sqlInsert)
                    print("nodegraph data updated in db")
                conn.commit()

                
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        conn.commit()
        conn.close()
        pygame.quit()
        quit()
        sys.quit()


    numText = basicfont.render("tileType: " + str(tileType),True,DARKRED)
    numTextRect = numText.get_rect()
    numTextRect.center = (50,20)
    
    Ntext = basicfont.render(str(north),True,DARKRED)
    NtextRect = Ntext.get_rect()
    NtextRect.center = ((C.SCREEN_WIDTH/2),20)

    Etext = basicfont.render(str(east),True,DARKRED)
    EtextRect = Etext.get_rect()
    EtextRect.center = ((C.SCREEN_WIDTH-20),(C.SCREEN_HEIGHT/2))

    Stext = basicfont.render(str(south),True,DARKRED)
    StextRect = Stext.get_rect()
    StextRect.center = ((C.SCREEN_WIDTH/2),(C.SCREEN_HEIGHT-20))

    Wtext = basicfont.render(str(west),True,DARKRED)
    WtextRect = Wtext.get_rect()
    WtextRect.center = (20,(C.SCREEN_HEIGHT/2))

    screen.fill((0,0,0))
    makeGrid(screen,C.SCREEN_WIDTH,C.SCREEN_HEIGHT,gridSize)

    all_walls.draw(screen)
    screen.blit(Ntext,NtextRect)
    screen.blit(Etext,EtextRect)
    screen.blit(Stext,StextRect)
    screen.blit(Wtext,WtextRect)
    screen.blit(numText,numTextRect)
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    snap_coord = snapToGrid(pos)
    if snap_coord != None:
        mouse_x = snap_coord[0] + 10
        mouse_y = snap_coord[1] + 10
        mouseRect = (mouse_x-11,mouse_y-11,mouse_x + 13,mouse_y + 13)
    if tileType == 1:
        screen.blit(STONE_IMAGE,mouseRect)
    elif tileType == 2:
        screen.blit(GRASS_IMAGE,mouseRect)
    elif tileType == 3:
        screen.blit(DIRT_IMAGE,mouseRect)
    elif tileType == 4:
        screen.blit(TILEFLOOR_IMAGE,mouseRect)
    elif tileType == 5:
        screen.blit(ROCKYGROUND_IMAGE,mouseRect)
    elif tileType == 6:
        screen.blit(WATER_IMAGE,mouseRect)
    else:
        screen.blit(NOTEXTURE_IMAGE,mouseRect)


    pygame.draw.circle(screen,DARKRED,[mouse_x+1,mouse_y+1],12,1)
    
    all_cursors.draw(screen)
    pygame.display.flip()
    clock.tick(60)
