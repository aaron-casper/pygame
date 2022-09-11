import pygame, math
import configuration as C
from utils import load_image

HERO_IMAGE = load_image('hero.png', 16, 16)
BIGSPLAT1 = load_image('bigsplat1.png', 25, 25)
all_bullets = pygame.sprite.Group()

def calculate_new_xy(old_xy,speed,angle_in_radians):
    #print("calcXY" + str(old_xy))
    new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
    new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
    return round(new_x), round(new_y)

class player(pygame.sprite.Sprite):
    def __init__(self,x,y, angle):
        self.score = 0
        self.dir = 0
        self.angle = 180
        self.speed = 0
        self.vel_x = 0
        self.vel_y = 0
        self.change_angle = 0
        self.health = 100
        self.firing = False
        self.canFire = True
        self.alive = True
        self.weapon = 1
        self.x = x
        self.y = y
        self.decel = False
        self.running = False
        self.mapID = 1
        self.ammo_pb = 15
        self.ammo_sh = 0
        self.ammo_mg = 0
        a = math.radians(self.dir)
        pygame.sprite.Sprite.__init__(self)
        PlayerSprite = pygame.Surface([15,15], pygame.SRCALPHA)
        self.image = pygame.transform.scale(HERO_IMAGE,(16,16))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(self.x,self.y))
#        self.image.fill((0,255,0))
        #shape = [(0,8), (3,0), (6,8)]
        #pygame.draw.lines(self.image,(255,0,0),False,shape, 4)

        self.collision = [False] * 9



    def update(self,speed,angle,all_goodies,all_monsters):
        self.x = self.x
        self.y = self.y
        if self.health >= 100:
            self.health = 100
        if self.ammo_mg >= 50:
            self.ammo_mg = 50
        if self.ammo_sh >= 25:
            self.ammo_sh = 25
        if self.ammo_pb >= 15:
            self.ammo_pb = 15
        #check for goodie pickup
        collide = pygame.sprite.spritecollideany(self,all_goodies)
        if collide:
            if collide.type == 0:
                self.health = self.health + 20
            if collide.type == 1:
                self.ammo_pb = self.ammo_pb + 30
            if collide.type == 2:
                self.ammo_sh = self.ammo_sh + 25
            if collide.type == 3:
                self.ammo_mg = self.ammo_mg + 50
            collide.kill()
        
        #update image rotation after a move
        self.image = pygame.transform.rotate(HERO_IMAGE,math.degrees(-angle))
        #print(angle)
        self.original_image = self.image
        if self.alive == False:
            self.image = BIGSPLAT1
            self.x = self.x
            self.y = self.y
            self.speed = 0
        self.rect = self.image.get_rect(center=(int(self.x),int(self.y)))
        if self.decel == True:
            while self.speed < 0:
                self.speed = self.speed + 0.1
                if self.speed > 0.2:
                    self.speed = 0
            while self.speed > 0:
                self.speed = self.speed - 0.1
                if self.speed < 0.2:
                    self.speed = 0


        self.rect = pygame.Rect([int(self.x),int(self.y),8,8])
        self.rect.center=calculate_new_xy(self.rect.center,int(self.speed),int(self.angle))
        #print(str(self.x) + " - " + str(self.y))
        self.surf = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.surf = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle += self.change_angle
        self.change_angle = 0
        self.angle = self.angle % 360
        self.vel_x = speed * math.cos(angle)
        self.vel_y = speed * math.sin(angle)
        self.y = self.y + self.vel_y
        self.x = self.x + self.vel_x
        if self.vel_x > 0:
            self.vel_x = self.vel_x * -0.1
        if self.vel_x < 0:
            self.vel_x = self.vel_x * 0.1
        if self.vel_y > 0:
            self.vel_y = self.vel_y * -0.1
        if self.vel_y < 0:
            self.vel_y = self.vel_y * 0.1
        if self.vel_y > 2:
            self.vel_y = 2
        if self.vel_x > 2:
            self.vel_x = 2
        if self.vel_y < -2:
            self.vel_y = -2
        if self.vel_x < -2:
            self.vel_x = -2
        return(self)

    def checkHit(self, rect):
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
        if self.running == True:
            correction = 2
        if self.collision[0] or self.collision[2] or self.collision[4]:
            self.x = self.x + correction

        if self.collision[1] or self.collision[3] or self.collision[5]:
            self.x = self.x - correction

        if self.collision[0] or self.collision[1] or self.collision[6]:
            self.y = self.y + correction

        if self.collision[2] or self.collision[3] or self.collision[7]:
            self.y = self.y - correction
            
    def checkMap(self):
        if self.x < 1:
            self.x = C.SCREEN_WIDTH - 15
            self.mapID = self.mapID - 1000
        if self.y < 1:
            self.y = C.SCREEN_HEIGHT - 15
            self.mapID = self.mapID + 1
        if self.x > C.SCREEN_WIDTH - 10:
            self.x = 1
            self.mapID = self.mapID + 1000
        if self.y > C.SCREEN_HEIGHT - 10:
            self.y = 1
            self.mapID = self.mapID - 1

