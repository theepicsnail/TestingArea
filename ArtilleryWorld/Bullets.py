import time
from math import hypot,atan2
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
    universe= None
    def __init__(self,universe,ttl):
        self.tod = time.time()+ttl
        self.universe = universe
        universe.addBullet(self)
        
    def step(self, dt):
        self.lx = self.x
        self.ly = self.y
        if time.time()>self.tod:
            return True
        self.x+=self.dx*dt
        self.y+=self.dy*dt
        self.distance += hypot(self.dx,self.dy)*dt
        acc = self.universe.calcAccel(self.x,self.y)
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
    def __init__(self, universe, splits = 3):
        Bullet.__init__(self,universe)
        self.splits = splits
        v = 255-85*splits
        self.color=[v,v,255]
    def step(self,dt):
        if Bullet.step(self,dt):
            return True
            
        if self.distance < 100:
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
            dist = hypot(self.dy,self.dx)*.5
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
        self.dropDist += 25

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
    color=[255,255,0]
    def hitPeak(self):
        dist = hypot(self.dy,self.dx)
        for i in xrange(16):
            b = SplitBullet(2)
            b.x=self.x
            b.y=self.y
            b.dx=self.dx+dist*cos(i*pi/8)
            b.dy=self.dy+dist*sin(i*pi/8)
        return True


class MarkerBullet(Bullet):
    deathTime = None
    def step(self,dt):
        if self.deathTime:
            return time.time()>self.deathTime
            
        if Bullet.step(self,dt):
            self.deathTime = time.time()+3

class AngleBullet(Bullet):
                
    def step(self,dt):
        dist = hypot(self.dy,self.dx)
        theta= atan2(self.dy,self.dx)
        for i in xrange(5):
            dtheta = .1*(i-2)
            b = MarkerBullet()
            b.x=self.x
            b.y=self.y
            b.dx=dist*cos(theta+dtheta)
            b.dy=dist*sin(theta+dtheta)        
        return True
class PowerBullet(Bullet):
                
    def step(self,dt):
        dist = hypot(self.dy,self.dx)
        theta= atan2(self.dy,self.dx)
        for i in xrange(5):
            dpow = i-2
            b = MarkerBullet()
            b.x=self.x
            b.y=self.y
            b.dx=(dist+dpow)*cos(theta)
            b.dy=(dist+dpow)*sin(theta)        
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

