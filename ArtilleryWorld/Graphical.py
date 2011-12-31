import pygame
from math import cos,sin,pi

class GraphicConfig:
    hudSurface=None
    mainSurface=None
    trailSurface=None
    font=None
    offset=(0,0)
    
def renderUniverse(gc,un):
    for p in un.planets:
        renderPlanet(gc,p)
    for p in un.players:
        renderPlayer(gc,p)
    for b in un.bullets:
        renderBullet(gc,b)

def renderHUD(gc,hud):
    #HUD
    ##Power meter
    pygame.draw.rect(gc.hudSurface,[0,255,0],(0,0,(hud.power-75)*2,20)) 
    pygame.draw.rect(gc.hudSurface,[255,255,255],(0,0,200,20),1)
    gc.hudSurface.blit(gc.font.render("Power: %i"%hud.power,0,[255,255,255]),(0,19))
    ##Direction meter
    pygame.draw.rect(gc.hudSurface,[0,255,0],(250,0,hud.direction*20,20))
    pygame.draw.rect(gc.hudSurface,[255,255,255],(250,0,125,20),1)
    gc.hudSurface.blit(gc.font.render("Angle: %2.1f"%hud.direction,0,[255,255,255]),(250,19))
    ## Current Weapon
    gc.hudSurface.blit(gc.font.render("Weapon: %r"%hud.weapon,0,[255,255,255]),(0,40))
    gc.hudSurface.blit(gc.font.render("Ammo: %r"%hud.ammo,0,[255,255,255]),(0,60))
    ## Active Bullets
    gc.hudSurface.blit(gc.font.render("Bullets: %i"%hud.bullets,0,[255,255,255]),(350,20))

    pass
        
def renderBullet(gc,b):
    pygame.draw.circle(gc.mainSurface,b.color, (int(b.x),int(b.y)),2)
    if b.lx:
        pygame.draw.line(gc.trailSurface,b.color,(int(b.lx),int(b.ly)),(int(b.x),int(b.y)))

def renderPlanet(gc,p):
        pygame.gfxdraw.filled_circle(gc.mainSurface,int(p.x),int(p.y),int(p.r-1),[100,100,100])

def renderPlayer(gc,p):
        #      0
        #     / \
        #    /   \
        #   /  .  \    . = (x,y)
        #  / _/ \_ \
        # /_/     \_\
        #//         \\
        #1           2
        points = [(10*cos(i*2*pi/3+p.direction)+p.x,10*sin(i*2*pi/3+p.direction)+p.y) for i in xrange(3)]
        points = [points[0],points[1],(p.x,p.y),points[2],points[0]]
        points = map(lambda x:map(int,x),points)
        pygame.draw.polygon(gc.mainSurface,p.color,points)
        gc.mainSurface.blit(gc.font.render("%5.2f"%p.dammage,0,[255,255,255]),map(int,(p.x,p.y)))

#def renderHUD(surface
