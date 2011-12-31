import random
from math import hypot,atan2,cos,sin,pi,sqrt
import pygame, sys
from pygame.locals import *
import pygame.gfxdraw
import time
from Bullets import *
from Player import *
from Universe import *
from Graphical import *
from HUD import *

pygame.init()
fpsClock = pygame.time.Clock()

display = pygame.display.set_mode((600,600))#Bottom most layer
trails = pygame.Surface((600,600),SRCALPHA)#This surface fades to transparent
window = pygame.Surface((600,600),SRCALPHA)#Top most layer 
hud    = pygame.Surface((600,30))

pygame.display.set_caption("CastleThing")
"""
def generateColor(f):#0<f<1
    g = f+1.0/3
    h = g+1.0/3
    return [127*(1+cos(f*2*pi)),127*(1+cos(g*2*pi)),127*(1+cos(h*2*pi))]
   """ 
    
universe = CreateUniverse()
gc = GraphicConfig()
gc.mainSurface = window
gc.trailSurface= trails
gc.hudSurface  = hud
gc.font = pygame.font.Font(None,20)
hud = HUD()

weapons={}
weapons[K_1]=Bullet
weapons[K_2]=SplitBullet
weapons[K_3]=AngleBullet
weapons[K_4]=CarpetBomb
weapons[K_5]=PineappleBomb
weapons[K_6]=Frag
weapons[K_7]=PowerBullet
weapons[K_p]=PlayerSpawn
ammo = {}
ammo[Bullet]=1000
ammo[SplitBullet]=10000
ammo[AngleBullet]=1000
ammo[PowerBullet]=1000
ammo[CarpetBomb]=100
ammo[PineappleBomb]=500
ammo[PlayerSpawn]=100
ammo[Frag]=1000
ammo[None]=0

p1 = Player(universe)
p1.x=90
p1.y=200
p1.color = [255,0,0]
player = p1

p2 = Player(universe)
p2.x=510
p2.y=400
p1.color = [128,64,192]

dt = 0

power = 121
keys = set()
curWep = None
TopLeft=(0,0)

while True:
    #Process events
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()  
        elif event.type == KEYDOWN:
            keys.add(event.key)
        elif event.type == KEYUP:
            if event.key in keys:#Possibly removed elsewhere
                keys.remove(event.key)
    
    if K_DOWN  in keys:  power = round(max(0,power-75-dt*30))+75
    if K_UP    in keys:  power = round(min(100,power-75+dt*30))+75
    if K_RIGHT in keys:  player.direction = round((player.direction+dt*2)%(2*pi),1)
    if K_LEFT  in keys:  player.direction = round((player.direction-dt*2)%(2*pi),1)

    dx=0
    dy=0
    if K_w in keys:
        dx=cos(player.direction)
        dy=sin(player.direction)
    if K_s in keys:
        dx=-cos(player.direction)
        dy=-sin(player.direction)
    if K_d in keys:
        dy=cos(player.direction)
        dx=-sin(player.direction)
    if K_a in keys:
        dy=-cos(player.direction)
        dx=sin(player.direction)
    player.x+=dx*dt*100
    player.y+=dy*dt*100
    TopLeft=p1.x/2,p1.y/2
    
    if K_SPACE in keys and curWep:
            if ammo[curWep] > 0:
                ammo[curWep]-=1
                b = curWep(universe)
                b.x=p1.x
                b.y=p1.y
                b.dx=cos(player.direction)*power
                b.dy=sin(player.direction)*power
            keys.remove(K_SPACE)
    wepSel = keys.intersection(weapons.keys())
    if wepSel:
        curWep = weapons[wepSel.pop()]
        hud.weapon=curWep
        hud.ammo=ammo[curWep]
    hud.power =power
    hud.direction=player.direction
    hud.bullets = len(universe.bullets)
        

    #Draw the screen
    display.fill([0,0,0])
    window.fill([0,0,0,0])
    trails.fill([1,1,1,1],None,BLEND_RGBA_SUB)

    #vector field
    if True:
        for x in xrange(0,600,10):
            for y in xrange(0,600,10):
                if random.random()>.001: continue
                
                acc = universe.calcAccel(x,y)
                if acc==None:continue
                x2 = int(x+acc[0]/5)
                y2 = int(y+acc[1]/5)
                pygame.draw.line(trails,[200,200,200],(x,y),(x2,y2))


    renderUniverse(gc,universe)
        
    for num,cnt in enumerate(ammo):
        pygame.draw.rect(window,[0,0,0],(0,num*5+20,ammo[cnt],5))
    
    renderHUD(gc,hud)
    #Do the physics
    universe.step(dt)


    pos = map(lambda x:-1*x,TopLeft)
    display.blit(trails,pos)
    display.blit(window,pos)
    pygame.display.update()
    dt = fpsClock.tick(30)/1000.0
















