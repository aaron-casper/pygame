#keyboard input module
import pygame
import sys
def update(player):
    self = player
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LSHIFT]:
        self.running = True

    if not pressed[pygame.K_LSHIFT]:
        self.running = False
        
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        self.change_angle = 0.1
        #self.vel_x = self.vel_x + 1
            
    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        self.speed += -1
            
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        self.change_angle = -0.1
        #self.vel_x = self.vel_x - 1 
            
    if pressed[pygame.K_UP] or pressed[pygame.K_w]:
        
        if self.running == True:
            self.speed += 2
        else:
            self.speed += 1

    if not pressed[pygame.K_UP]:
        self.decel = True

    if not pressed[pygame.K_DOWN]:
        self.decel = True
        
        
    if pressed[pygame.K_ESCAPE]:
        print("escape! escape! or something")
        pygame.quit()
        quit()
        sys.quit()
    return(self)
