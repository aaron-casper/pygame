import pygame
import configuration as C
import keyinput
import gameCore
display = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))#, FULLSCREEN )isplay = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))#, FULLSCREEN )
pygame.display.set_caption("splatter!")
pygame.display.init()
info = pygame.display.Info()
pygame.mouse.set_visible(True)

#basicfont = pygame.font.Font('assets/open24.ttf',20)
#basicfont2 = pygame.font.Font('assets/open24.ttf',180)

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

while True:
    draw_rect_alpha(display, (128,128,128, 64), (20,20,(C.SCREEN_WIDTH - 20),(C.SCREEN_HEIGHT - 20)))
    pygame.display.flip()
