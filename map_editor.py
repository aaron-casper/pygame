import sys
import pygame
import sqlite3
import maps
database = "./maps.db"
conn = sqlite3.connect(database)
sqlCreate = """CREATE TABLE IF NOT EXISTS levels (
                id integer PRIMARY KEY,
                mapID interger NOT NULL,
                levelData blob NOT NULL,
                north integer NOT NULL,
                east integer NOT NULL,
                south integer NOT NULL,
                west integer NOT NULL
                );"""
cur = conn.cursor()
cur.execute(sqlCreate)
conn.close()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("map_editor")
basicfont = pygame.font.SysFont(None,20)
pygame.mouse.set_visible(False)
all_walls = pygame.sprite.Group()
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
gridSize = 20

class wall(pygame.sprite.Sprite):
    def __init__(self,tileposx,tileposy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([gridSize,gridSize])
        self.image.fill((128,128,128))
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
    if 0 < mousePos[0] < SCREEN_WIDTH and 0 < mousePos[1] < SCREEN_HEIGHT:
        return roundCoords(mousePos[0],mousePos[1])
        

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
nextRecord = "SELECT MapID FROM levels ORDER BY MapID DESC LIMIT 1;"
data = cur.execute(nextRecord)
for item in data:
    nextRecord = int(item[0])
    mapID = nextRecord

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
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y))
            if event.key == 100:
                mapID = mapID + 1000
                for item in all_walls:
                    item.kill()
                levelData = maps.loadMap(mapID)
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y))
            if event.key == 115:
                mapID = mapID - 1
                for item in all_walls:
                    item.kill()
                levelData = maps.loadMap(mapID)
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y))
            if event.key == 97:
                mapID = mapID - 1000
                for item in all_walls:
                    item.kill()
                levelData = maps.loadMap(mapID)
                for item in levelData:
                    x = item[0]
                    y = item[1]
                    #print(x)
                    #print(y)
                    all_walls.add(wall(x,y))
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            snap_coord = snapToGrid(pos)
            if snap_coord != None:
                mouse_x = snap_coord[0] + 10
                mouse_y = snap_coord[1] + 10
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(str(event.button) + " DOWN")
            if event.button == 1:
                wall(snap_coord[0],snap_coord[1])                        
            if event.button == 3:
                for item in all_walls:
                    if item.x == snap_coord[0] and item.y == snap_coord[1]:
                        item.kill()
            if event.button == 4:
                for item in all_walls:
                    item.kill()
                mapID = mapID - 1
                if mapID < 1:
                    mapID = 1
                levelData = maps.loadMap(mapID)
                for item in levelData:
                    x = item[0]
                    y = item[1]
                   # print(x)
                    #print(y)
                    all_walls.add(wall(x,y))
            if event.button == 5:
                for item in all_walls:
                    item.kill()
                mapID = mapID + 1
                levelData = maps.loadMap(mapID)
                for item in levelData:
                    x = item[0]
                    y = item[1]
                   # print(x)
                   # print(y)
                    all_walls.add(wall(x,y))
            if event.button == 2:
                levelData = ""
                for item in all_walls:
                    levelData = levelData + (str(item.x) + "," + str(item.y) + "|")
                    conn = sqlite3.connect(database)
                    cur = conn.cursor()
                sqlInsert = "INSERT INTO levels (levelData,mapID,north,east,south,west) VALUES ('" + str(levelData) + "'," + str(mapID) + "," + str(north) + "," + str(east) + "," + str(south) + "," + str(west) + ");"
                cur.execute(sqlInsert)
                sqlInsert = "UPDATE levels SET levelData = '" + str(levelData) + "' WHERE mapID = " + str(mapID) + ";"
                print(sqlInsert)
                cur.execute(sqlInsert)
                conn.commit()
                conn.close()
            #if event.type == pygame.MOUSEBUTTONUP:
            #print(str(event.button) + " UP") 
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
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


    numText = basicfont.render("Map #: " + str(mapID),True,GREEN)
    numTextRect = numText.get_rect()
    numTextRect.center = (30,20)
    
    Ntext = basicfont.render(str(north),True,GREEN)
    NtextRect = Ntext.get_rect()
    NtextRect.center = ((SCREEN_WIDTH/2),20)

    Etext = basicfont.render(str(east),True,GREEN)
    EtextRect = Etext.get_rect()
    EtextRect.center = ((SCREEN_WIDTH-20),(SCREEN_HEIGHT/2))

    Stext = basicfont.render(str(south),True,GREEN)
    StextRect = Stext.get_rect()
    StextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT-20))

    Wtext = basicfont.render(str(west),True,GREEN)
    WtextRect = Wtext.get_rect()
    WtextRect.center = (20,(SCREEN_HEIGHT/2))

    screen.fill((0,0,0))
    makeGrid(screen,SCREEN_WIDTH,SCREEN_HEIGHT,gridSize)

    all_walls.draw(screen)
    screen.blit(Ntext,NtextRect)
    screen.blit(Etext,EtextRect)
    screen.blit(Stext,StextRect)
    screen.blit(Wtext,WtextRect)
    screen.blit(numText,numTextRect)
    pygame.draw.circle(screen,RED,[mouse_x,mouse_y],3,3)
    pygame.display.flip()
    clock.tick(60)
