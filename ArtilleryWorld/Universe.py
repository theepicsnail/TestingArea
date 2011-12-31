import random
from math import hypot,atan2,cos,sin

#Acceleration felt from a planet is calculated as:
#G * (radius/distance)^2
G = 100 

class Universe:

    players = []
    bullets = []
    planets = []
    def step(self,dt):
        deadBullets = []
        for b in self.bullets:            
            if b.step(dt):
                deadBullets.append(b)
            else:
                for p in self.players:
                    if hypot(b.x-p.x,b.y-p.y)<=11 and b.distance>11:
                        p.hit(b)
                        deadBullets.append(b)
        map(self.bullets.remove,deadBullets)

    def addPlanet(self,p):
        self.planets.append(p)

    def addBullet(self,b):
        self.bullets.append(b)
    def removeBullet(self,b):
        self.bullets.remove(b)
        
    def addPlayer(self,p):
        self.players.append(p)
    def removePlayer(self,p):
        self.players.remove(p)
        
    def calcAccel(self,x,y):
        acc = [0,0]
        for p in self.planets:
            dist = hypot(p.y-y,p.x-x)
            if dist <= p.r: 
                return None
            theta= atan2(p.y-y,p.x-x)
            acc[0] += p.r**2*cos(theta)/dist**2
            acc[1] += p.r**2*sin(theta)/dist**2
            
        return acc[0]*G,acc[1]*G #G's were factored out.
    
def CreateUniverse():
    import Planet   
    u = Universe()    
    for n in xrange(10):
        if random.random()>.5: continue
        p= Planet.Planet()
        p.x=100+400*random.random()
        p.y=100+400*random.random()
        p.r=20+80*random.random()
        u.addPlanet(p)
    return u
    
