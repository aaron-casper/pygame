import random

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
import keyinput
import playerChar
import monsters 
import maps

pygame.init()
basicfont = pygame.font.SysFont(None,20)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("tile_engine")

playerPositionX = 250
playerPositionY = 250
tileposx = 0
tileposy = 0

all_walls = pygame.sprite.Group()
all_players = pygame.sprite.Group()
all_monsters = pygame.sprite.Group()

clock = pygame.time.Clock()
mapID = 1
#game classes and code
class wall(pygame.sprite.Sprite):
    def __init__(self,tileposx,tileposy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20,20])
        self.image.fill((128,128,128))
        self.x = tileposx
        self.y = tileposy
        self.rect = pygame.Rect([self.x,self.y,20,20])        


#create objects, player, monster, level



PlayerOne = playerChar.player(100,100,0)
all_players.add(PlayerOne)
randomMonster = monsters.randomMonster(500,500,0)
all_monsters.add(randomMonster)


levelData = maps.loadMap(PlayerOne.mapID)
for item in levelData:
    x = item[0]
    y = item[1]
    all_walls.add(wall(x,y))

while True:
    if PlayerOne.mapID != mapID:
        mapID = PlayerOne.mapID
        levelData = maps.loadMap(PlayerOne.mapID)
        for item in all_walls:
            item.kill()
        for item in levelData:
            x = item[0]
            y = item[1]
            #print(x)
            #print(y)
            all_walls.add(wall(x,y))
    numText = basicfont.render(str(int(PlayerOne.x)) + ", " + str(int(PlayerOne.y)),True,GREEN)
    numTextRect = numText.get_rect()
    numTextRect.center = (80,20)
    screen.fill((0,0,0))    
    for block in all_walls:
        PlayerOne.checkHit(block.rect)
        randomMonster.checkHit(block.rect)
    for monster in all_monsters:
        PlayerOne.checkHit(monster.rect)
    keyinput.update(PlayerOne)
    PlayerOne.update(PlayerOne.speed,PlayerOne.angle)
    randomMonster.update(randomMonster.speed,randomMonster.angle)
    screen.blit(numText,numTextRect)
    all_walls.draw(screen)
    all_monsters.draw(screen)
    all_players.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    
    #PlayerOne.rect = PlayerOne.update(PlayerOne.speed,PlayerOne.angle)
