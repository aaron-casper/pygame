import random
#from OpenGL.GL import *
from pygame.locals import *
import sys
#sys.setrecursionlimit(2000)

from datetime import datetime
import time
from pygame import font
import pygame
import csv
import numpy as np
from numpy import loadtxt
import math


#import game components
import menu
import goodies
import keyinput
import playerChar
import monsters
import maps
import pellet
import weapons
import splat
from utils import load_image
import configuration as C

pygame.init()
basicfont = pygame.font.Font('assets/open24.ttf',20)
basicfont2 = pygame.font.Font('assets/open24.ttf',180)


display = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))#, FULLSCREEN )
pygame.display.set_caption("splatter!")
pygame.display.init()
info = pygame.display.Info()
pygame.mouse.set_visible(True) 


#func to draw alpha'd rectangle
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

#create the clock
clock = pygame.time.Clock()

#create offscreen surface to render to
offscreen_surface = pygame.Surface((info.current_w, info.current_h))
print("loading sprites")
WATER_IMAGE = load_image('water.png', 25, 25)
DIRT_IMAGE = load_image('dirt.png', 25, 25)
GRASS_IMAGE = load_image('grass.png', 25, 25)
STONE_IMAGE = load_image('stone.png', 25, 25)
TILEFLOOR_IMAGE = load_image('tilefloor.png',25,25)
ROCKYGROUND_IMAGE = load_image('rockyground.png',25,25)
NOTEXTURE_IMAGE = load_image('notexture.png',25,25)
MONSTER_IMAGE = load_image('monster.png', 20, 20)
print("loaded sprites")
tileposx = 0
tileposy = 0

print("creating sprite groups")
all_walls = pygame.sprite.Group()
all_players = pygame.sprite.Group()
all_monsters = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_terrain = pygame.sprite.Group()
all_splats = pygame.sprite.Group()
all_goodies = pygame.sprite.Group()
print("created sprite groups")


gameOverText = basicfont2.render("",True,C.RED)
gameOverTextRect = gameOverText.get_rect()
gameOverTextRect.center = (450,300)
#draw_rect_alpha(offscreen_surface, (0,0,0, 64), gameOverTextRect)

mapID = 1
#game classes and code
class wall(pygame.sprite.Sprite):
    def __init__(self,tileposx,tileposy,tileType):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,25])
        self.image.fill((128,128,128))
        self.x = tileposx
        self.y = tileposy
        self.tileType = tileType
        if self.tileType == 1:
            self.image = STONE_IMAGE
        else:
            self.image.fill(C.RED)
        self.rect = pygame.Rect([self.x,self.y,25,25])

class terrain(pygame.sprite.Sprite):
    def __init__(self,tileposx,tileposy,tileType):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,25])
        self.image.fill((128,128,128))
        self.x = tileposx
        self.y = tileposy
        self.tileType = tileType
        if self.tileType == 1:
            self.image.fill(C.GREY)
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
            self.image = NOTEXTURE_IMAGE
        self.rect = pygame.Rect([self.x,self.y,25,25])


#create objects, player, monster, level
aiWalls = []
aiNodes = []
aiWallNodes = []
def levelChange(mapID): 
    for item in all_monsters:
        item.kill()
    for item in all_walls:
        item.kill()
    for item in all_splats:
        item.kill()
    for item in all_terrain:
        item.kill()
    for item in all_goodies:
        item.kill()
    levelData = maps.loadMap(mapID)
       
    for item in levelData:
        x = item[0]
        y = item[1]
        tileType = item[2]
        #build AI map of walls
        if tileType != 1:
            all_terrain.add(terrain(x,y,tileType))
        elif tileType == 1:
            all_walls.add(wall(x,y,tileType))
        
    #quit()
def addMonsters(numMonsters, mapID):
    for item in all_monsters:
        item.kill()
    numCritters = (len(all_walls) + len(all_terrain)) / 3
    i = 0
    while i < numMonsters:
        i = i + 1
        randomMonster = monsters.randomMonster(random.randint(100,900),random.randint(100,600),0, MONSTER_IMAGE,mapID)
        all_monsters.add(randomMonster)

def gameLoop(mapID):

    #spawn the player
    PlayerOne = playerChar.player(C.playerStartPositionX,C.playerStartPositionY,0)
    #add to player list
    all_players.add(PlayerOne)
    levelChange(1)
    addMonsters(1,mapID)

    while True:
        if len(all_monsters) == 0:
            PlayerOne.score = PlayerOne.score + 1
            #PlayerOne.health = 100
            #addMonsters(PlayerOne.score * 3, mapID)
            addMonsters(1, mapID)
        #get key input
        keyinput.update(PlayerOne)

        #shoot the guns
        if (PlayerOne.firing == True):
            #weapons code here, split into new module
            weapons.fire(PlayerOne,all_bullets)
        PlayerOne.checkMap()
        if PlayerOne.mapID != mapID:
            mapID = PlayerOne.mapID
            levelChange(mapID)
            addMonsters(1, mapID)
            #addMonsters(PlayerOne.score * 3, mapID)
        
        numText = basicfont.render(str(int(PlayerOne.health)) + " hp | BUL: " + str(PlayerOne.ammo_pb) + " | SHL: " + str(PlayerOne.ammo_sh) + " | MG: " + str(PlayerOne.ammo_mg) + " | Weapon: " + str(PlayerOne.weapon) + " | Score: " + str(PlayerOne.score),True,C.WHITE)
        numTextRect = numText.get_rect()
        numTextRect.center = (500,20)
  
        #update wall/collision for player
        for block in all_walls:
            PlayerOne.checkHit(block.rect)

        #update monsters/ai
        for monster in all_monsters:
            monster.update(0.5,monster.angle,all_players,PlayerOne,monster.nodeGraph,all_splats,all_goodies,mapID,all_walls)
            PlayerOne.checkHit(monster.rect)

        #check player vars - should be moved to PlayerChar.py

        
        for bullet in all_bullets:
            bullet.update(all_walls,all_monsters)
        #player died, reset and restart at map 1
        PlayerOne.update(PlayerOne.speed,PlayerOne.angle,all_goodies,all_monsters)
        if PlayerOne.health <= 0:
            for item in all_monsters:
                item.kill()
            for item in all_goodies:
                item.kill()
            levelChange(1)
            PlayerOne.health = 100
            PlayerOne.score = PlayerOne.score - 1
            PlayerOne.ammo_pb = 15
            PlayerOne.ammo_sh = 0
            PlayerOne.ammo_mg = 0
            PlayerOne.x = C.playerStartPositionX
            PlayerOne.y = C.playerStartPositionY
            PlayerOne.update(PlayerOne.speed,PlayerOne.angle,all_goodies,all_monsters)
        #draw the stuff to screen
        display.fill((0,0,0))
        all_terrain.draw(display)
        all_splats.draw(display)
        all_walls.draw(display)
        all_goodies.draw(display)
        all_monsters.draw(display)
        all_players.draw(display)
        all_bullets.draw(display)
    
        #HUD
        draw_rect_alpha(display, (0,0,0, 64), numTextRect)
        display.blit(numText,numTextRect)
        display.blit(gameOverText,gameOverTextRect)
 
        #flip display buffer/display new frame
        pygame.display.flip()
        #clock.tick(60)

gameLoop(1)       
