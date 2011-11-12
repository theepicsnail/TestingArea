import pygame, sys
from pygame.locals import *
from math import sin,cos,pi
pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((1360,768))
pygame.display.set_caption("Pygame sample.")


black=pygame.Color(  0,  0,  0)
white=pygame.Color(255,255,255)

fontObj = pygame.font.Font('freesansbold.ttf', 32)

msg = 'Hello world.'

def ring(surface, color, (x,y), r, thickness=5, angle=0, length=2*pi, edges=30):
    points = []
    for i in xrange(edges):
        dx = cos(angle + i*length/(edges+2.0) + angle)
        dy = sin(angle + i*length/(edges+2.0) + angle)
        points.append((x+dx*r    ,y+dy*r    ))
        points.insert(0,(x+dx*(r+thickness),y+dy*(r+thickness)))

    pygame.draw.polygon(surface,color,points)

def color(a):
    val = lambda x:int((sin(x)+1)*127)
    return (val(a),val(a+2*pi/3),val(a+4*pi/3))

#pygame.display.toggle_fullscreen()
center = (680,384)

def end():
#    pygame.display.toggle_fullscreen()
    pygame.quit()
    sys.exit()        
    
angle = 0
pressed=[]
while True:
    windowSurfaceObj.fill(white)
    for event in pygame.event.get():
        if event.type == QUIT:
            end()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                end()
            pressed.append(event.key)
        elif event.type == KEYUP:
            pressed.remove(event.key)
    if K_LEFT in pressed:
        angle += .1
    if K_RIGHT in pressed:
        angle -= .1
    print pygame.mouse.get_pressed() 
    t = pygame.time.get_ticks()/1000.0 
    ring(windowSurfaceObj, color(angle), center, 200, 20, angle, 1.0)
    pygame.display.update()
    fpsClock.tick(30)
    
