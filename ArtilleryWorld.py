import random
from math import hypot,atan2,cos,sin,pi,sqrt
import pygame, sys
from pygame.locals import *
import pygame.gfxdraw
import time

pygame.init()
fpsClock = pygame.time.Clock()

display = pygame.display.set_mode((600,600))
window = pygame.Surface(display.get_size(),SRCALPHA)
trails = pygame.Surface(window.get_size(),SRCALPHA)#This surface fades to transparent

pygame.display.set_caption("CastleThing")

background = [255,255,0,0]
font = pygame.font.Font(None,20)

def generateColor(f):#0<f<1
    g = f+1.0/3
    h = g+1.0/3
    return [127*(1+cos(f*2*pi)),127*(1+cos(g*2*pi)),127*(1+cos(h*2*pi))]


class Player:
    x = 0
    y = 0
    color = [255,0,0]
    def hit(self):
        print "hit."
class Planet:
    x = 0
    y = 0
    r = 0
class Bullet:
    x = 0
    y = 0
    dx= 0
    dy= 0
    tod = 0
    lx = None
    ly = None
    distance = 0 # distance gone (sum of steps)
    color=[255,255,255]
    def __init__(self,ttl=30):
        bullets.append(self)
        self.tod = time.time()+ttl
        
    def step(self, dt):
        self.lx = self.x
        self.ly = self.y
        if time.time()>self.tod:
            return True
        self.x+=self.dx*dt
        self.y+=self.dy*dt
        self.distance += hypot(self.dx,self.dy)*dt
        acc = calcAccel(self.x,self.y)
        if acc == None:
            return True
        self.dx += acc[0]*dt
        self.dy += acc[1]*dt
        return False
    
class AltitudeBullet(Bullet):
    lastVel = None
    peaked = False
    
    def step(self, dt):
        if Bullet.step(self,dt):
            return True
        v = hypot(self.dy,self.dx)
        ret = False
        if self.lastVel:
            if v>self.lastVel and not self.peaked:
                ret = self.hitPeak()
                self.peaked = True
        self.lastVel = v
        return ret        
    def hitPeak(self):
        return False
        
class SplitBullet(Bullet):
    splitTime=0
    splits = 0
    def __init__(self, splits = 3):
        Bullet.__init__(self)
        self.splitTime = time.time()+.5
        self.splits = splits
    def step(self,dt):
        if Bullet.step(self,dt):
            return True
            
        if time.time()<self.splitTime:
            return False
        if self.splits == 0 :
            return False
            
        #split!
        dist = hypot(self.dy,self.dx)
        theta= atan2(self.dy,self.dx)
        t1 = theta+.1
        t2 = theta-.1
        b = SplitBullet(self.splits-1)
        b.x=self.x
        b.y=self.y
        b.dx=dist*cos(t1)
        b.dy=dist*sin(t1)
        
        b = SplitBullet(self.splits-1)
        b.x=self.x
        b.y=self.y
        b.dx=dist*cos(t2)
        b.dy=dist*sin(t2)
        return True
        

class Frag(Bullet):
    color=[255,0,0]
    def step(self,dt):
        if Bullet.step(self,dt):
            dist = hypot(self.dy,self.dx)
            self.x-=self.dx*dt
            self.y-=self.dy*dt
            for i in xrange(32):
                b = Bullet()
                b.x=self.x
                b.y=self.y
                b.dx=dist*cos(i*pi/16)
                b.dy=dist*sin(i*pi/16)
            return True

       

class CarpetBomb(Bullet):
    splitTime=0
    splits = 0
    color=[255,0,0]
    dropDist = 50
    def __init__(self):
        Bullet.__init__(self)
    def step(self,dt):
        if Bullet.step(self,dt):
            return True
        if self.distance < self.dropDist:
            return False
        self.dropDist += 10

        dist = hypot(self.dy,self.dx)*0
        theta= atan2(self.dy,self.dx)
        t1 = theta+pi/2
        t2 = theta-pi/2
        b = Bullet()
        b.x=self.x
        b.y=self.y
        b.dx=dist*cos(t1)
        b.dy=dist*sin(t1)
        
        b = Bullet()
        b.x=self.x
        b.y=self.y
        b.dx=dist*cos(t2)
        b.dy=dist*sin(t2)
        return False

        
        

class PineappleBomb(AltitudeBullet):
    def hitPeak(self):
        dist = hypot(self.dy,self.dx)
        for i in xrange(32):
            b = Bullet()
            b.x=self.x
            b.y=self.y
            b.dx=self.dx+dist*cos(i*pi/16)
            b.dy=self.dy+dist*sin(i*pi/16)
        return True



class FanBullet(Bullet):
    class MarkerBullet(Bullet):
        deathTime = None
        def step(self,dt):
            if self.deathTime:
                return time.time()>self.deathTime
                
            if Bullet.step(self,dt):
                self.deathTime = time.time()+3
                
    def step(self,dt):
        dist = hypot(self.dy,self.dx)
        theta= atan2(self.dy,self.dx)
        for i in xrange(5):
            dtheta = .1*(i-2)
            b = self.MarkerBullet()
            b.x=self.x
            b.y=self.y
            b.dx=dist*cos(theta+dtheta)
            b.dy=dist*sin(theta+dtheta)        
        return True


class PlayerSpawn(Bullet):
    def step(self,dt):
        if Bullet.step(self,dt):
            p = Player()
            p.x = self.x
            p.y = self.y
            p.color = generateColor(random.random())
            players.append(p)
            return True
        return False
weapons={}
weapons[K_1]=Bullet
weapons[K_2]=SplitBullet
weapons[K_3]=FanBullet
weapons[K_4]=CarpetBomb
weapons[K_5]=PineappleBomb
weapons[K_6]=Frag
weapons[K_p]=PlayerSpawn
ammo = {}
ammo[Bullet]=1000
ammo[SplitBullet]=10000
ammo[FanBullet]=1000
ammo[CarpetBomb]=100
ammo[PineappleBomb]=500
ammo[PlayerSpawn]=100
ammo[Frag]=1000

p1 = Player()
p1.x=90
p1.y=200
p1.color = generateColor(0)

p2 = Player()
p2.x=510
p2.y=400
p1.color = generateColor(.5)


pl1= Planet()
pl1.x=400
pl1.y=400
pl1.r=100

pl2= Planet()
pl2.x=200
pl2.y=200
pl2.r=100


players = [p1,p2]
planets = [pl1,pl2]

bullets = []
    
G = 100#gravity is calculated at G*r^2/dist^2
def calcAccel(x,y):
    acc = [0,0]
    for p in planets:
        dist = hypot(p.y-y,p.x-x)
        if dist <= p.r: 
            return None
        theta= atan2(p.y-y,p.x-x)
        acc[0] += p.r**2*cos(theta)/dist**2
        acc[1] += p.r**2*sin(theta)/dist**2
        
    return acc[0]*G,acc[1]*G #G's were factored out.
dt = 0


direction = 1.7
power = 90
keys = set()
curWep = None

while True:

    #Process events
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()  
        elif event.type == KEYDOWN:
            keys.add(event.key)
            if event.key==K_SPACE:
                fire = True
        elif event.type == KEYUP:
            if event.key in keys:
                keys.remove(event.key)
    
    if K_DOWN  in keys:  power = round(max(0,power-dt*30))
    if K_UP    in keys:  power = round(min(300,power+dt*30))
    if K_RIGHT in keys:  direction = round((direction+dt*2)%(2*pi),1)
    if K_LEFT  in keys:  direction = round((direction-dt*2)%(2*pi),1)
    if K_SPACE in keys and curWep:
            if ammo[curWep] > 0:
                ammo[curWep]-=1
                b = curWep()
                b.x=p1.x
                b.y=p1.y
                b.dx=cos(direction)*power
                b.dy=sin(direction)*power
            keys.remove(K_SPACE)
    wepSel = keys.intersection(weapons.keys())
    if wepSel:
        curWep = weapons[wepSel.pop()]
    

    #Draw the screen
    display.fill([0,0,0])
    window.fill([0,0,0,0])
    trails.fill([1,1,1,1],None,BLEND_RGBA_SUB)

    #vector field
    if True:
        for x in xrange(0,600,10):
            for y in xrange(0,600,10):
                if random.random()>.001: continue
                
                acc = calcAccel(x,y)
                if acc==None:continue
                x2 = int(x+acc[0]/5)
                y2 = int(y+acc[1]/5)
                pygame.draw.line(trails,[200,200,200],(x,y),(x2,y2))



    for p in planets:
        pygame.gfxdraw.filled_circle(display,p.x,p.y,p.r-1,[100,100,100])
#        pygame.gfxdraw.aacircle(window,p.x,p.y,p.r,[100,100,100])
#        pygame.gfxdraw.aacircle(window,[0,0,255], (p.x,p.y), p.r)

    for p in players:
        pygame.draw.circle(window,p.color, map(int,(p.x,p.y)), 10)
        
    for num,cnt in enumerate(ammo):
        pygame.draw.rect(window,[0,0,0],(0,num*5+20,ammo[cnt],5))
        
    #HUD
    ##Direction Marker
    pygame.draw.line(window,[0,0,0], (p1.x,p1.y), (int(p1.x+cos(direction)*10),int(p1.y+sin(direction)*10)))
    ##Power meter
    pygame.draw.rect(window,[0,255,0],(0,0,power*2/3,20)) 
    pygame.draw.rect(window,[255,255,255],(0,0,200,20),1)
    window.blit(font.render("Power: %i"%power,0,[255,255,255]),(0,19))
    ##Direction meter
    pygame.draw.rect(window,[0,255,0],(250,0,direction*20,20))
    pygame.draw.rect(window,[255,255,255],(250,0,125,20),1)
    window.blit(font.render("Angle: %2.1f"%direction,0,[255,255,255]),(250,19))


    #Do the physics
    deadBullets = []
    for b in bullets:
        
        if b.step(dt):
            deadBullets.append(b)
        else:
            for p in players:
                if hypot(b.x-p.x,b.y-p.y)<=11 and b.distance>11:
                    p.hit()
                    deadBullets.append(b)
            pygame.draw.circle(window,b.color, (int(b.x),int(b.y)),2)
            pygame.draw.line(trails,b.color,(int(b.lx),int(b.ly)),(int(b.x),int(b.y)))
    
    map(bullets.remove,deadBullets)
    display.blit(trails,(0,0))
    display.blit(window,(0,0))
    pygame.display.update()
    dt = fpsClock.tick(30)/1000.0
















