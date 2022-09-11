#splatter effect
import random
import pygame
from utils import load_image
SMALLSPLAT1 = load_image('smallsplat1.png', 10, 10)
SMALLSPLAT2 = load_image('smallsplat2.png', 20, 10)
SMALLSPLAT3 = load_image('smallsplat3.png', 10, 10)
BIGSPLAT1 = load_image('bigsplat1.png', 25, 25)
BIGSPLAT2 = load_image('bigsplat2.png', 25, 25)
BIGSPLAT3 = load_image('bigsplat3.png', 25, 25)
class splat(pygame.sprite.Sprite):
    def __init__(self,tileposx,tileposy,bigSplat):
        pygame.sprite.Sprite.__init__(self)
        if bigSplat != True:
            splatChooser = random.randint(0,2)
            if splatChooser == 0:
                self.image = pygame.transform.rotate(SMALLSPLAT1,random.randint(0,360))
            elif splatChooser == 1:
                self.image = pygame.transform.rotate(SMALLSPLAT2,random.randint(0,360))
            elif splatChooser == 2:
                self.image = pygame.transform.rotate(SMALLSPLAT3,random.randint(0,360))
            self.x = tileposx
            self.y = tileposy
            self.rect = pygame.Rect([self.x,self.y,10,10])
        elif bigSplat == True:
            self.image = BIGSPLAT1
            splatChooser = random.randint(0,2)
            if splatChooser == 0:
                self.image = pygame.transform.rotate(BIGSPLAT1,random.randint(0,360))
            elif splatChooser == 1:
                self.image = pygame.transform.rotate(BIGSPLAT2,random.randint(0,360))
            elif splatChooser == 2:
                self.image = pygame.transform.rotate(BIGSPLAT3,random.randint(0,360))
            self.x = tileposx
            self.y = tileposy
            self.rect = pygame.Rect([self.x,self.y,25,25])

