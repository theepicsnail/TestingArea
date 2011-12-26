
from math import hypot,atan2,cos,sin,pi
import pygame, sys
from pygame.locals import *
import time

pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((600,600))
pygame.display.set_caption("CastleThing")

background = [255,255,255]

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
    steps = 0
    def __init__(self,ttl=10):
        bullets.append(self)
        self.tod = time.time()+ttl
        
    def step(self, dt):
        if time.time()>self.tod:
            return True
        self.x+=self.dx*dt
        self.y+=self.dy*dt
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

class CarpetBomb(Bullet):
    splitTime=0
    splits = 0
    def __init__(self):
        Bullet.__init__(self)
        self.splitTime = time.time()+.6
    def step(self,dt):
        if Bullet.step(self,dt):
            return True
            
        if time.time()<self.splitTime:
            return False
        
        self.splitTime = time.time()+.1
        
        #split!
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

weapons={}
weapons[K_1]=Bullet
weapons[K_2]=SplitBullet
weapons[K_3]=FanBullet
weapons[K_4]=CarpetBomb
weapons[K_5]=PineappleBomb
ammo = {}
ammo[Bullet]=1000
ammo[SplitBullet]=500
ammo[FanBullet]=1000
ammo[CarpetBomb]=100
ammo[PineappleBomb]=500



p1 = Player()
p1.x=150
p1.y=250
p1.color = generateColor(0)

p2 = Player()
p2.x=450
p2.y=250
p1.color = generateColor(.5)


pl1= Planet()
pl1.x=300
pl1.y=400
pl1.r=200

pl2= Planet()
pl2.x=200
pl2.y=200
pl2.r=20


players = [p1,p2]
planets = [pl1]

bullets = []
    
G = 1#gravity is calculated at G*r^2/dist^2
def calcAccel(x,y):
    acc = [0,0]
    for p in planets:
        dist = hypot(p.y-y,p.x-x)
        if dist <= p.r: 
            return None
        theta= atan2(p.y-y,p.x-x)
        acc[0] += p.r**2*cos(theta)/dist
        acc[1] += p.r**2*sin(theta)/dist
        
    return acc[0]*G,acc[1]*G #G's were factored out.
dt = 0


direction = 0
power = 0
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
    
    if K_DOWN  in keys:  power = max(0,power-dt*30)
    if K_UP    in keys:  power = min(300,power+dt*30)
    if K_RIGHT in keys:  direction = (direction+dt*2)%(2*pi)
    if K_LEFT  in keys:  direction = (direction-dt*2)%(2*pi)
    if K_SPACE in keys and curWep:
            if ammo[curWep] > 0:
                ammo[curWep]-=1
                b = curWep()
                b.x=p1.x
                b.y=p1.y
                b.dx=cos(direction)*power
                b.dy=sin(direction)*power
                print power
    wepSel = keys.intersection(weapons.keys())
    if wepSel:
        curWep = weapons[wepSel.pop()]
    

    #Draw the screen
    window.fill(background)

    for p in planets:
        pygame.draw.circle(window,[0,0,255], (p.x,p.y), p.r)

    for p in players:
        pygame.draw.circle(window,p.color, (p.x,p.y), 10)
        
    for num,cnt in enumerate(ammo):
        pygame.draw.rect(window,[0,0,0],(0,num*5+20,ammo[cnt],5))
    pygame.draw.line(window,[0,0,0], (p1.x,p1.y), (int(p1.x+cos(direction)*power),int(p1.y+sin(direction)*power)))
    pygame.draw.rect(window,[0,255,0],(0,0,power*2/3,20)) 
    pygame.draw.rect(window,[0,255,0],(250,0,direction*20,20))
    pygame.draw.rect(window,[0,0,0],(0,0,200,20),1)
    pygame.draw.rect(window,[0,0,0],(250,0,120,20),1)


    #Do the physics
    deadBullets = []
    for b in bullets:
        if b.step(dt):
            deadBullets.append(b)
        else:
            for p in players:
                if hypot(b.x-p.x,b.y-p.y)<=11 and b.steps > 1:
                    p.hit()
                    deadBullets.append(b)
            pygame.draw.circle(window,[0,0,0], (int(b.x),int(b.y)),2)
    
    map(bullets.remove,deadBullets)

        
    pygame.display.update()
    dt = fpsClock.tick(30)/1000.0
















