#AI functions
import configuration as C
import pygame
import random
import math

def facePlayer(self,player,walls):
    if player.alive == True:
        self = self
        player = player
        walls = walls
        xdiff = player.x - self.x
        ydiff = player.y - self.y
        self.angle = math.atan2(ydiff,xdiff)
    else:
        self.change_angle = random.randint(-1,1)
    return(self)

def moveToGoal(self,player,walls):
    self.speed = 1
    

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
    #return(self)
        
def attack(self,player):
    if player.health <= 0:
        return()
    self.attacking = True
