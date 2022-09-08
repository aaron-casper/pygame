import pygame
import random
import configuration as C
from utils import load_image

HEALTH_IMAGE = load_image("healthbox.png", 20,20)
PB_AMMO = load_image("pb_box.png",20,20)
SH_AMMO = load_image("sh_box.png", 20,20)
MG_AMMO = load_image("mg_box.png", 20,20)

class goodieBox(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20,20])
        self.x = x
        self.y = y
        itemType = random.randint(0,3)
        self.type = itemType
        if itemType == 0:
            self.image = HEALTH_IMAGE
        if itemType == 1:
            self.image = PB_AMMO
        if itemType == 2:
            self.image = SH_AMMO
        if itemType == 3:
            self.image = MG_AMMO
        self.rect = pygame.Rect([self.x,self.y,20,20])

    
