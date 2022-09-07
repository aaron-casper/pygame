import pygame
import math
WHITE = (196,128,0)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, start_x, start_y, dest_x, dest_y,angle):
        super(Bullet,self).__init__()
        #drawing geometries and some other goodies
        self.image = pygame.Surface([2, 2])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        # because rect.x and rect.y are automatically converted to integers, we need to create different variables that
        # store the location as floating point numbers. int is not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y
        # calculating the angle in radians between the start points and end points.
        #x_diff = dest_x - start_x
        #y_diff = dest_y - start_y
        #angle = math.atan2(y_diff, x_diff);
        # taking into account the angle, calculate our change_x and change_y. velocity is how fast the bullet travels.
        velocity = 10
        self.angle = angle
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity
    def update(self,all_walls,all_monsters):
        # floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
        # rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # if bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()
        wallCollide = pygame.sprite.spritecollide(self, all_walls, False)
        for wall in wallCollide:
            self.kill()    
        monsterCollide = pygame.sprite.spritecollide(self, all_monsters, False)
        for monster in monsterCollide:
            monster.health = monster.health - 10
            monster.bleeding = True
        

