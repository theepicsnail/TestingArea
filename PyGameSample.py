import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption("Pygame sample.")


red  =pygame.Color(255,  0,  0)
white=pygame.Color(255,255,255)

fontObj = pygame.font.Font('freesansbold.ttf', 32)

msg = 'Hello world.'

while True:
    windowSurfaceObj.fill(red)
    pygame.draw.circle(windowSurfaceObj,white, (200,200),100,50)
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()        
    pygame.display.update()
    fpsClock.tick(30)

