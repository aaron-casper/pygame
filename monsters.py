import pygame
import math
import random
from utils import load_image
import configuration as C
import ai

MONSTER_IMAGE = load_image('monster.png', 15, 15)
sight_distance = 100

def calculate_new_xy(old_xy,speed,angle_in_radians):
    #print("calcXY" + str(old_xy))
    new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
    new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
    return round(new_x), round(new_y)

class randomMonster(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,image):
        self.dir = 0
        self.angle = random.randint(0,360)
        self.speed = 0.5
        self.vel_x = 0
        self.vel_y = 0
        self.change_angle = 0
        self.health = 100
        self.bleeding = False
        self.image = image
        self.attacking = False
        self.x = x
        self.y = y
        self.decel = False
        self.running = False
        a = math.radians(self.dir)
        pygame.sprite.Sprite.__init__(self)
        monsterSprite = pygame.Surface([15,15], pygame.SRCALPHA)
        self.image = pygame.transform.scale(self.image,(15,15))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.collision = [False] * 9

    def update(self,speed,angle,player,all_walls):
        if self.health <= 0:
            self.kill()
        xdiff = player.x - self.x
        ydiff = player.y - self.y
        if (abs(xdiff) < 10) and (abs(ydiff) < 10) and (player.health > 0):
            self.attacking = True
        if (abs(xdiff) > 10) or (abs(ydiff) > 10) or (player.health < 1):
            self.attacking = False
        #get angle
        ai.facePlayer(self,player,all_walls)
        ai.moveToGoal(self,player,all_walls)
        #collide with anything?
        collide = pygame.sprite.spritecollideany(self,all_walls)
        if collide: 
            ai.bumpWall(self,collide)
            self.angle = self.angle + self.change_angle
        #screen edges
        correction = 1
        if self.x < 1:
            self.x = self.x + correction
            self.angle = self.angle - 180

        if self.y < 1:
            self.y = self.y + correction
            self.angle = self.angle - 180
        if self.x > C.SCREEN_WIDTH - 15:
            self.x = self.x - correction
            self.angle = self.angle - 180

        if self.y > C.SCREEN_HEIGHT - 15:
            self.y = self.y - correction
            self.angle = self.angle - 180
        #update after a move
        self.image = pygame.transform.rotate(MONSTER_IMAGE,math.degrees(-angle))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(int(self.x),int(self.y)))
        self.rect = pygame.Rect([int(self.x),int(self.y),8,8])
        self.rect.center=calculate_new_xy(self.rect.center,int(self.speed),int(self.angle))
        self.surf = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.surf = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.y = self.y + self.vel_y
        self.x = self.x + self.vel_x
        return(self)

