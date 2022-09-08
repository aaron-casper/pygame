import sys
import pygame
import sqlite3
import maps
from utils import load_image
import configuration as C

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

pygame.init()

WATER_IMAGE = load_image('water.png', 25, 25)
DIRT_IMAGE = load_image('dirt.png', 25, 25)
GRASS_IMAGE = load_image('grass.png', 25, 25)
STONE_IMAGE = load_image('stone.png', 25, 25)

screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
pygame.display.set_caption("map_editor")
basicfont = pygame.font.SysFont(None,20)
pygame.mouse.set_visible(False)
all_walls = pygame.sprite.Group()
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
            self.image.fill(WHITE)
        elif self.tileType == 5:
            self.image.fill(YELLOW)
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
    print("filling blank map with grass")
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

mapID = 1
getGroup()
color = (128,128,128)
clock = pygame.time.Clock()
conn = sqlite3.connect(database)
cur = conn.cursor()
levelData = maps.loadMap(mapID)
tileType = 1
if len(levelData) < 1 :
    fillNewMap()
    
for item in levelData:
    x = item[0]
    y = item[1]
    tileType = item[2]
    all_walls.add(wall(x,y,tileType))

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
                if tileType < 1:
                    tileType = 1
            if event.button == 5:
                tileType = tileType + 1
            if event.button == 2:
                levelData = ""
                for item in all_walls:
                    levelData = levelData + (str(item.x) + "," + str(item.y) + "," + str(item.tileType) + "|")
                    conn = sqlite3.connect(database)
                    cur = conn.cursor()
                try:
                    sqlInsert = "INSERT INTO levels (levelData,mapID,north,east,south,west) VALUES ('" + str(levelData) + "'," + str(mapID) + "," + str(north) + "," + str(east) + "," + str(south) + "," + str(west) + ");"
                    cur.execute(sqlInsert)
                except:
                    sqlInsert = "UPDATE levels SET levelData = '" + str(levelData) + "' WHERE mapID = " + str(mapID) + ";"
                    cur.execute(sqlInsert)
                conn.commit()
                
            #if event.type == pygame.MOUSEBUTTONUP:
            #print(str(event.button) + " UP") 
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        conn.commit()
        conn.close()
        pygame.quit()
        quit()
        sys.quit()
  #  if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
  #      mapID = mapID + 1000
            
  #  if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
  #      mapID = mapID -1
            
  #  if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
   #     mapID = mapID - 1000
            
    #if pressed[pygame.K_UP] or pressed[pygame.K_w]:
     #   mapID = mapID + 1


    numText = basicfont.render("tileType: " + str(tileType),True,DARKRED)
    numTextRect = numText.get_rect()
    numTextRect.center = (30,20)
    
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
    if tileType == 1:
        pygame.draw.circle(screen,GREY,[mouse_x,mouse_y],10,0)
    elif tileType == 2:
        pygame.draw.circle(screen,GREEN,[mouse_x,mouse_y],10,0)
    elif tileType == 3:
        pygame.draw.circle(screen,BROWN,[mouse_x,mouse_y],10,0)
    elif tileType == 4:
        pygame.draw.circle(screen,WHITE,[mouse_x,mouse_y],10,0)
    elif tileType == 5:
        pygame.draw.circle(screen,YELLOW,[mouse_x,mouse_y],10,0)
    elif tileType == 6:
        pygame.draw.circle(screen,PURPLE,[mouse_x,mouse_y],10,0)
    else:
        pygame.draw.circle(screen,RED,[mouse_x,mouse_y],10,0)
        if tileType > 7:
            tileType = 7
    pygame.draw.circle(screen,DARKRED,[mouse_x,mouse_y],10,1)
    pygame.display.flip()
    clock.tick(60)
