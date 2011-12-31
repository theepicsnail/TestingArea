import pygame, sys
from pygame.locals import *
from math import *
from random import shuffle,randint,random
pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((640,480))
pygame.display.set_caption("Pygame sample.")

black=pygame.Color(  0,  0,  0)
white=pygame.Color(255,255,255)

UP,DOWN,LEFT,RIGHT = range(4)
SPACE,SOLID,HUMAN,ZOMBIE = range(4)    
colors = [(255,255,255),(0,0,0),(0,255,0),(0,0,128)]

class Cell:
    color = (0,0,0)
    def step(self,world):
        return True
    def canEnter(self):
        return True
    def canAttack(self):
        return False
class AttackableCell(Cell):
    underAttack = False  #Gets set to true if you were attacked during the last update.
    attack = 0
    health = 100
    dmg    = 0
    def alive(self):
        return self.health > self.dmg
    def canEnter(self):
        return False
    def canAttack(self):
        return True
    def dammage(self,dmg):
        self.underAttack = True
        self.dmg += dmg
        return self.health <= self.dmg
    def getAttack(self): #Whoevers attack is higher wins the cell.
        return self.attack

class SPACE(Cell):
    color = (255,255,255)
class SOLID(Cell):
    canEnter = lambda x:False
class HUMAN(AttackableCell):
    attack = 10
    breedChance = .2
    health = 100
    color  = (0,255,0)
    age    = 0
    def step(self,world):
        self.age = self.age+1
        self.dmg += .1
        self.attack += .01
        return self.alive()
    def breed(self,other):
        print "Breed"
        if self.age<10 or other.age<10: return
        if random()>(self.breedChance+other.breedChance)/2: return        
        merge = lambda a,b:(a+b)*(.9+.2*random())/2
        child = HUMAN()
        child.attack = merge(other.attack,self.attack)
        child.health = merge(other.health,self.health)
        child.breedChance = merge(other.breedChance,self.breedChance)
        self.dmg += 10
        other.dmg += 10
        print child.attack, child.health
        return child
    def attackHuman(self):
        return random()<.3
class ZOMBIE(AttackableCell):
    attack = 5
    health = 75
    color = (255,0,0)
    def step(self,world):
        self.dmg += .1
        return self.alive()
    def convert(self,src):
        z = ZOMBIE()
        z.attack = self.attack*(random()*.1+.9)
        z.health = src.health*.75*(random()*.1+.9)
        return z
def drawCells(world):
    global window,colors
    size = 20
    for r,row in enumerate(world):
        for c,v in enumerate(row):
            pygame.draw.rect(window,v.color,(c*size,r*size,size,size))
            
def humanStep(r,c,world):
    global LEFT,RIGHT,UP,DOWN
    l = [ LEFT,RIGHT,UP,DOWN]
    if isinstance(world[r+1][c],ZOMBIE):
        return DOWN
    if isinstance(world[r][c-1],ZOMBIE):
        return LEFT
    if isinstance(world[r][c+1],ZOMBIE):
        return RIGHT
    if isinstance(world[r-1][c],ZOMBIE):
        return UP
    shuffle(l)
    
    world[r][c].underAttack = False#reset that flag
    return l[0]

def zombieStep(r,c,world):
    global LEFT,RIGHT,UP,DOWN
    l = [ LEFT,RIGHT,UP,DOWN, None,None,None,None]
    if world[r][c].underAttack:            
        if isinstance(world[r+1][c],AttackableCell):
            return DOWN
        if isinstance(world[r][c-1],AttackableCell):
            return LEFT
        if isinstance(world[r][c+1],AttackableCell):
            return RIGHT
        if isinstance(world[r-1][c],AttackableCell):
            return UP
        world[r][c].underAttack = False
    shuffle(l)
    return l[0]

def updateCells(world):
    stats = []
    moves= []
    for r,row in enumerate(world):
        for c,v in enumerate(row):
            m = None
            if not v.step(world):
                world[r][c] = SPACE()
                continue
            if isinstance(v,HUMAN):
                stats.append((HUMAN, v.health, v.attack))
                m = humanStep(r,c,world)
            elif isinstance(v,ZOMBIE):
                stats.append((ZOMBIE, v.health, v.attack))
                m = zombieStep(r,c,world)
                
            if m!=None:
                moves.append((m,r,c))
    
    shuffle(moves)

    dead = []
    for m,r,c in moves:
        if (r,c) in dead: continue
        
        d=None
        if m == LEFT:
            d = (0,-1)
        elif m==RIGHT:
            d = (0,1)
        elif m==UP:
            d = (-1,0)
        elif m==DOWN:
            d = (1,0)
        targPos = (d[0]+r,d[1]+c)
        targ = world[targPos[0]][targPos[1]]
        doMove = False
        died = False
        if isinstance(targ,HUMAN) and isinstance(world[r][c],HUMAN):
            print "Human collision",world[r-d[0]][c-d[1]],r-d[0],c-d[1]
            if world[r][c].attackHuman():
                died = targ.dammage(world[r][c].getAttack())
                if died:
                    doMove = True
                    dead.append(targPos)    
            elif isinstance(world[r-d[0]][c-d[1]],SPACE):
                child = world[r][c].breed(targ)
                if child:
                    world[r-d[0]][c-d[1]] = child
                continue
            
        elif isinstance(targ,ZOMBIE) and isinstance(world[r][c],ZOMBIE):
            continue
        else:    
            if targ.canEnter():
                doMove = True
            elif targ.canAttack():
                print "attack!"
                died = targ.dammage(world[r][c].getAttack())
                if isinstance(targ,HUMAN):
                    died = False
                    world[targPos[0]][targPos[1]] = world[r][c].convert(targ)

            if died:
                doMove = True
                dead.append(targPos)
        
            
        if doMove:
            #del world[d[0]][d[1]]
            world[targPos[0]][targPos[1]] = world[r][c]
            world[r][c] = SPACE()
    return stats
    
    


    
world=[[]]
world[0] = [SOLID()]*20
world += [[SOLID()]+[SPACE()]*18+[SOLID()] for x in range(18)]
world += [[SOLID()]*20]
for n in xrange(1,5):
    world[n][n] = HUMAN()
world[-2][-2]=ZOMBIE()

humanDrop = True
from time import time
lastTime = time()
while True:
    if time()-lastTime > 5:
        r,c = randint(0,19),randint(0,19)
        if isinstance(world[r][c],SPACE):
            cls = HUMAN if humanDrop else ZOMBIE
            world[r][c] = cls()

        humanDrop = not humanDrop
        lastTime = time()
        
        
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()      
    
    window.fill(white)
    
    stats = updateCells(world)
    drawCells(world)
    for n,(spec, health, attack) in enumerate(stats):
        color = (255,0,0)
        if spec == HUMAN:
            color = (0,255,0)
            
        pygame.draw.line(window,color,(400,n*1),(400+int(health),n*1),1)
    pygame.display.update()
    fpsClock.tick(30)

    
    
