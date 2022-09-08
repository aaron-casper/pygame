import pellet
import random
import pygame
import configuration as C

def delayInFire(delay):
    ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() < (ticks + delay):
        None

def fire(PlayerOne,all_bullets):
    self = PlayerOne
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    i = 0
        #pistol
    if self.weapon == 1:
        if self.ammo_pb > 1:
            pew = pellet.Bullet((self.x), (self.y), mouse_x, mouse_y,self.angle)
            all_bullets.add(pew)
            self.firing = False
            self.ammo_pb = self.ammo_pb - 1
        elif self.ammo_pb <= 0:
            self.weapon =- 1
            self.ammo_pb = 0
            
        #shotgun
    if self.weapon == 2:
        if self.ammo_sh > 1:
            while i < C.SHOTGUNPELLETS:
                i = i + 1
                pew = pellet.Bullet((self.x), (self.y), mouse_x, mouse_y,(self.angle + random.uniform(-C.SHOTGUNACCURACY,C.SHOTGUNACCURACY)))
                all_bullets.add(pew)
            self.firing = False
            self.ammo_sh = self.ammo_sh - 1
        elif self.ammo_sh <= 0:
            self.ammmo_sh = 0
            self.weapon =- 1
        #smg
    if self.weapon == 3:
        if self.ammo_mg > 1:
        #TODO; make 3 round burst work
            pew = pellet.Bullet((self.x), (self.y), mouse_x, mouse_y,self.angle)
            all_bullets.add(pew)
            self.ammo_mg = self.ammo_mg - 1
            #self.firing = False
        elif self.ammo_mg <= 0:
            self.ammo_mg = 0
            self.weapon =- 1
        
            
        #state engine limits
    if self.weapon >= 4:
        self.weapon = 1
    if self.weapon <= 0:
        self.weapon = 3
        
