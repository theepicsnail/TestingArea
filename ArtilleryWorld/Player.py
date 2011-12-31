from math import hypot
class Player:
    def __init__(self,universe):
        self.universe= universe
        universe.addPlayer(self)
    x = 0
    y = 0
    color = [255,0,0]
    dammage = 0
    direction = 4.9
    def hit(self,b):
        dmg = hypot(b.dx,b.dy)
        self.dammage += dmg
        print "Hit.",dmg
        if self.dammage >= 10000:
            universe.removePlayer(self)
            for i in xrange(64):
                b = Bullet()
                factor = random.random()*5+10
                b.dx=factor*10*cos(i*pi/32)
                b.dy=factor*10*sin(i*pi/32)
                b.x=self.x+b.dx/factor#each player is r=10px
                b.y=self.y+b.dy/factor

