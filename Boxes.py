import pygame, sys
from pygame.locals import *
from math import *
pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption("Pygame sample.")


black=pygame.Color(  0,  0,  0)
white=pygame.Color(255,255,255)

RIGHT,UP,LEFT,DOWN = [pi*i/2 for i in range(4)]
gravityDir = DOWN
def drawGravityMeter(surface,x,y,r):
    pygame.draw.circle(surface,black,(x,y),r)
    pygame.draw.circle(surface,white,(x,y),r-3)
    pygame.draw.line(surface,black,(x,y),(x+cos(gravityDir)*r,y-sin(gravityDir)*r))


boxes = [ (0,0,100,10), (0,10,10,90) ]

def getWorldSurface():
    s = pygame.Surface((640,480))
    s.fill(white)
    for r in boxes:
        pygame.draw.rect(s,black,r)
    return s


wsurf = getWorldSurface()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()      
    pygame.display.update()
    fpsClock.tick(30)

    windowSurfaceObj.fill(white)
    windowSurfaceObj.blit(wsurf,(640-480,0))
    drawGravityMeter(windowSurfaceObj,20,20,20)
    
    
    pygame.draw.circle(windowSurfaceObj,white, (200,200),100,50)
    








