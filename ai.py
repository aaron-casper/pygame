#AI functions
import configuration as C
import pygame
import random
import math
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import sqlite3
database = "maps.db"
conn = sqlite3.connect(database)

def loadNodeGraph(mapID):
    aiWalls = []
    allWalls = []
    row = []
    sqlQuery = "SELECT nodeGraph FROM nodeGraphs WHERE mapID = " + str(mapID) + ";"
    cur = conn.cursor()
    nodeGraphData = cur.execute(sqlQuery)
    for item in nodeGraphData:
        #print(item)
        #print("item")
        item = str(item).replace(',','')
        item = str(item).split('|')
        
        y = 1
        firstLine = str(item[0]).replace('(','')
        firstLine = firstLine.replace('(','')
        firstLine = firstLine.replace("'",'')
        aiWalls.append(firstLine)
        while y < len(item) - 1:
            row = []
            x = 0
            while x < len(item[y]):
                #print(item[y][x],end='')
                row.append(int(item[y][x]))
                x += 1
            #print('')
            aiWalls.append(row)
            y += 1
        #print(aiWalls)
    return(aiWalls) #path array or x/y tuples
    

    
def findPath(self,player,nodeGraph):
    matrix = nodeGraph
    #print(len(matrix))
    grid = Grid(matrix = matrix)
    x = int(self.x)
    y = int(self.y)
    if x <= 0:
        x = 1
    if y <= 0:
        y = 1
    px = int(player.x)
    py = int(player.y)
    if px <= 0:
        px = 1
    if py <= 0:
        py = 1
    px = px // 25
    py = py // 25
    x = x // 25
    y = y // 25
    start = grid.node(x,y)
    end = grid.node(px,py)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
    path, runs = finder.find_path(start,end,grid)
    print(grid.grid_str(path=path,start=start,end=end))
    #print(path)
    return(path)

def facePlayer(self):
    x = int(self.x) // 25
    y = int(self.y) // 25
    if len(self.path) > 1:
        xdiff = self.path[0][0] - x
        ydiff = self.path[0][1] - y
        self.angle = math.atan2(ydiff,xdiff)
        #print("pos: " + str((x,y)) + "targ: " + str(self.path[1]))
        self.path.pop(0)
    return(self)
    

def bumpWall(self,wall):
    rect = wall.rect
    self.collision[0] = rect.collidepoint(self.rect.topleft)
    self.collision[1] = rect.collidepoint(self.rect.topright)
    self.collision[2] = rect.collidepoint(self.rect.bottomleft)
    self.collision[3] = rect.collidepoint(self.rect.bottomright)

    self.collision[4] = rect.collidepoint(self.rect.midleft)
    self.collision[5] = rect.collidepoint(self.rect.midright)
    self.collision[6] = rect.collidepoint(self.rect.midtop)
    self.collision[7] = rect.collidepoint(self.rect.midbottom)

    self.collision[8] = rect.collidepoint(self.rect.center)
    correction = 1
    if self.collision[0] or self.collision[2] or self.collision[4]:
        self.x = self.x + correction
        self.change_angle = 0.1
    if self.collision[1] or self.collision[3] or self.collision[5]:
        self.x = self.x - correction
        self.change_angle = -0.1
    if self.collision[0] or self.collision[1] or self.collision[6]:
        self.y = self.y + correction
        self.change_angle = 0.1
    if self.collision[2] or self.collision[3] or self.collision[7]:
        self.y = self.y - correction
        self.change_angle = -0.1
    return(self)
        
def attack(self,player):
    if player.health <= 0:
        return()
    self.attacking = True
