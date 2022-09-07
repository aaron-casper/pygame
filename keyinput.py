#keyboard input module
import pygame
import sys
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick_count = pygame.joystick.get_count()
xAxis = 0
yAxis = 0

for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    axes = joystick.get_numaxes()
    
def update(player):
    self = player
    if self.alive == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.canFire = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.canFire = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.canFire == True:
                        self.firing = True
                        #print("pew")
                    elif self.canFire == False:
                        self.firing = False
                        #print("no pew")
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    self.running = True
                if event.button == 4:
                    self.weapon = 1
                if event.button == 5:
                    self.weapon = 2
                if event.button == 0:
                    if self.canFire == True:
                        self.firing = True
                    elif self.canFire == False:
                        self.firing = False
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    self.canFire == True
                if event.button == 1:
                    self.running = False
        
    
        #print(xAxis)
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LSHIFT]:
            self.running = True

        #if not pressed[pygame.K_LSHIFT]:
        #    self.running = False
        
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.change_angle = 0.1
            #self.vel_x = self.vel_x + 1
            
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.speed += -1
            
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.change_angle = -0.1
            #self.vel_x = self.vel_x - 1 
            
        if pressed[pygame.K_1]: 
            self.weapon = 1
        if pressed[pygame.K_2]:
            self.weapon = 2

        
        
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.speed += 1
            
        if pressed[pygame.K_SPACE]:
            if self.canFire == True:
                self.firing = True
                #print("pew")
            elif self.canFire == False:
                self.firing = False
                #print("no pew")

        if not pressed[pygame.K_SPACE]:
            self.canFire == True
        
        if not pressed[pygame.K_UP]:
            self.decel = True

        if not pressed[pygame.K_DOWN]:
            self.decel = True

        Xaxis = joystick.get_axis(0)
        Yaxis = joystick.get_axis(1)
        self.change_angle = (Xaxis * 0.1)
        if self.running == True:
            self.speed = (Yaxis * -1) + 1
        else:
            self.speed = Yaxis * -1

        if pressed[pygame.K_ESCAPE]:
            print("escape! escape! or something")
            pygame.quit()
            quit()
            sys.quit()

    elif self.alive == False:
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            print("escape! escape! or something")
            pygame.quit()
            quit()
            sys.quit()


    return(self)
