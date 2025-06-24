import pygame,sys,math,random
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
global w,h
w,h = 1000,800
win = pygame.display.set_mode((w,h),RESIZABLE)
pygame.display.set_caption('physics')

backwards = False

def dotProduct(vec1,vec2):
    return vec1[0]*vec2[0]+vec1[1]*vec2[1]
        
def collideWall(o1,w,h):
    if o1.pos['x']-o1.radius<0 or o1.pos['x']+o1.radius>w:
        o1.vel['x'] = -o1.vel['x']
    if o1.pos['y']-o1.radius<0 or o1.pos['y']+o1.radius>h:
        o1.vel['y'] = -o1.vel['y']

def createPairs(l):
    pairs = []
    for n in range(len(l)-1):
        for x in range(n+1,len(l)):
            pairs.append((l[n],l[x]))
    return pairs      


def collide(o1,o2):
    absDistSqr = (o1.pos['x'] - o2.pos['x'])**2+(o1.pos['y'] - o2.pos['y'])**2
    if absDistSqr <= (o1.radius+o2.radius)**2:
        normalVec = [o2.pos['x']-o1.pos['x'],o2.pos['y']-o1.pos['y']]
        v1 = [o1.vel['x'],o1.vel['y']]
        v2 = [o2.vel['x'],o2.vel['y']]
        absVal = math.sqrt(normalVec[0]**2 + normalVec[1]**2)
        uNormalVec = [normalVec[0]/absVal,normalVec[1]/absVal]
        uTan = [-uNormalVec[1],uNormalVec[0]]
        v1n = dotProduct(uNormalVec,v1)
        v2n = dotProduct(uNormalVec,v2)
        v1t = dotProduct(uTan,v1)
        v2t = dotProduct(uTan,v2)
        nv1n,nv2n,nv1t,nv2t = v2n,v1n,v1t,v2t
        vnv1n = [nv1n*uNormalVec[0],nv1n*uNormalVec[1]]
        vnv2n = [nv2n*uNormalVec[0],nv2n*uNormalVec[1]]
        vnv1t = [nv1t*uTan[0],nv1t*uTan[1]]
        vnv2t = [nv2t*uTan[0],nv2t*uTan[1]]
        nv1 = [vnv1n[0]+vnv1t[0],vnv1n[1]+vnv1t[1]]
        nv2 = [vnv2n[0]+vnv2t[0],vnv2n[1]+vnv2t[1]]
        o1.vel['x'],o1.vel['y'] = nv1[0],nv1[1]
        o2.vel['x'],o2.vel['y'] = nv2[0],nv2[1]
        o1.collided = True
        o2.collided = True
        
        
        
class Particle:
    def __init__(self,radius,velx,vely,x,y):
        self.pos = {'x':x,'y':y}
        self.vel = {'x':velx,'y':vely}         
        self.acc = {'x':0,'y':0}
        self.radius = radius
        self.controlled = False
        self.collided = False
        
    def update(self):
        self.pos['x']+=self.vel['x'] 
        self.pos['y']+=self.vel['y'] 
        self.vel['x']+=self.acc['x'] 
        self.vel['y']+=self.acc['y'] 
        if self.controlled:
            pygame.draw.circle(win,(255,0,0),(int(self.pos['x']),int(self.pos['y'])),self.radius)
        else:
            pygame.draw.circle(win,(0,0,0),(int(self.pos['x']),int(self.pos['y'])),self.radius)
        
def control(o):
    global backwards
    k = pygame.key.get_pressed()
    speed = 0.01
    if k[pygame.K_UP]:
        o.vel['y']-=speed
    if k[pygame.K_DOWN]:
        o.vel['y']+=speed
    if k[pygame.K_RIGHT]:
        o.vel['x']+=speed
    if k[pygame.K_LEFT]:
        o.vel['x']-=speed
    if k[pygame.K_s]:
        o.vel['x']*=1.01
        o.vel['y']*=1.01
    if k[pygame.K_r] and not backwards:
        for obj in objList:
            obj.vel['x'] = -obj.vel['x']
            obj.vel['y'] = -obj.vel['y']
        backwards = True
    elif k[pygame.K_e] and backwards:
        for obj in objList:
            obj.vel['x'] = -obj.vel['x']
            obj.vel['y'] = -obj.vel['y']
        backwards = False
    o.controlled = True

'''a = Particle(10,0,0,50,50)   
b = Particle(10,0,0,400,50)   
c = Particle(10,0,0,200,50)   '''   
    
objList = []
for x in range(10):
    for y in range(10):
        objList.append(Particle(20,0,0,60+60*x,60+60*y))
        
pairList = createPairs(objList)
ye = True
run = True
mouse = (650,650)
while run:
    if ye:
        wx,hx = 1000,1000
        ye = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            mouse = event.pos
        if event.type==pygame.VIDEORESIZE:
            wx,hx = event.size
            win = pygame.display.set_mode((wx,hx),RESIZABLE)
    win.fill((255,255,255))
    control(objList[0])
    pygame.draw.line(win,(0,0,0),(mouse[0],0),mouse)
    pygame.draw.line(win,(0,0,0),mouse,(0,mouse[1]))
    for x in objList:
        x.update()
    for y in objList:
        collideWall(y,mouse[0],mouse[1])
    for pair in pairList:
        collide(pair[0],pair[1])
    '''a.update()
    b.update()
    c.update()
    collideWall(a)
    collideWall(b)
    collideWall(c)
    collide(a,b)
    collide(b,c)
    collide(a,c)
    a.update()
    b.update()
    c.update()
    control(a)'''
    for n in objList:
        n.update()
        '''if n.collided:
            n.vel['x']*=0.9
            n.vel['y']*=0.9
            n.collided = False'''
    clock.tick(60000)
    pygame.display.update()
        
pygame.quit()
sys.exit() 