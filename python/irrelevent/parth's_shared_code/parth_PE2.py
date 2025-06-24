import math,sys,pygame
from pygame.locals import *

pygame.init()
w,h = 1000,800
win = pygame.display.set_mode((w,h))
center = [w//2,h//2]
screenCenter = center
clock = pygame.time.Clock()
global rateOfTime
rateOfTime = 0
t0 = 0
tf = 0
dt = tf - t0

def rectToMagDir(x,y):
    mag = math.sqrt(x*x+y*y)
    if mag == 0:
        sintheta = 1
        costheta = 0
    else:
        sintheta = y/mag
        costheta = x/mag
    return (mag, sintheta, costheta)

def resolveComponents(magnitude,sintheta,costheta):
    perpendicular = magnitude*sintheta
    along = magnitude*costheta
    return along, perpendicular

class Object: 
    def __init__(self,x,y,mass,size):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = mass
        self.size = size
        self.forces = []
        
    def draw(self):
        myX = center[0] + (simScale*self.x)
        myY = center[1] - (simScale*self.y)
        if myX > 2000:
            myX = 2000
        if myY > 2000:
            myY = 2000
        if myX < -2000:
            myX = -2000
        if myY < -2000:
            myY = -2000
        myX, myY = int(myX), int(myY)
        pygame.draw.rect(win,(0,0,0),(myX,myY,simScale*self.size,simScale*self.size),1)
    
    def exert(self,xF,yF,obj):
        obj.forces.append((xF,yF))
    
    def evalForces(self):
        netXF = 0; netYF = 0
        for f in self.forces:
            netXF += f[0]
            netYF += f[1]
        
        self.vx += netXF*dt/self.mass
        self.vy += netYF*dt/self.mass
        
        if self.x < 1000000000 and self.x > -1000000000:    
            self.x += self.vx*dt
        if self.y < 1000000000 and self.y > -1000000000:  
            self.y += self.vy*dt
        self.forces = []
    
def g(obj,value):
    obj.exert(0,value*obj.mass,obj)
    if abs(obj.y-obj.size-ground.y) < 0.1 and obj.x < ground.x+ground.size:
        obj.vy = 0
        obj.y = obj.size + ground.y+0.1
        ground.exert(0,-obj.mass*value,obj)

class Wedge():
    def __init__(self,x,y,mass):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = mass
        self.forces = []
        
    def draw(self):
        pygame.draw.line(win,(0,0,0),(center[0]+int(simScale*self.x[0]),center[1] - int(simScale*self.y[0])),((center[0]+int(simScale*self.x[1])),(center[1] - int(simScale*self.y[1]))),1)
        pygame.draw.line(win,(0,0,0),(center[0]+int(simScale*self.x[1]),center[1] - int(simScale*self.y[1])),((center[0]+int(simScale*self.x[2])),(center[1] - int(simScale*self.y[2]))),1)
        pygame.draw.line(win,(0,0,0),(center[0]+int(simScale*self.x[2]),center[1] - int(simScale*self.y[2])),((center[0]+int(simScale*self.x[0])),(center[1] - int(simScale*self.y[0]))),1)
    
    def exert(self,xF,yF,obj):
        obj.forces.append((xF,yF))
    
    def evalForces(self):
        netXF = 0; netYF = 0
        for f in self.forces:
            netXF += f[0]
            netYF += f[1]
        self.vx += netXF*dt/self.mass
        self.vy += netYF*dt/self.mass
        for x in self.x:
            if x < 1000000 and x > -1000000:
               x += self.vx*dt
        for y in self.y:
            if y < 1000000 and y > -1000000:
                y += self.vy*dt
        self.forces = []
    
class Spring:
    def __init__(self,obj1,obj2,nl,k,turns,damping=0):
        self.k = k
        self.damp = damping
        self.turns = turns
        self.obj1 = obj1
        self.obj2 = obj2
        self.x1 = obj1.x + obj1.size*0.5
        self.y1 = obj1.y + obj1.size*0.5
        self.x2 = obj2.x + obj2.size*0.5
        self.y2 = obj2.y + obj2.size*0.5
        self.sintheta = 0
        self.costheta = 1
        self.nl = nl
        
    def evalForces(self):
        self.x1 = self.obj1.x + self.obj1.size*0.5
        self.y1 = self.obj1.y - self.obj1.size*0.5
        self.x2 = self.obj2.x + self.obj2.size*0.5
        self.y2 = self.obj2.y - self.obj2.size*0.5
        d = math.sqrt((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)
        self.disp = d - self.nl

        if not d == 0:
            self.sintheta = (self.y2 - self.y1)/d
            self.costheta = (self.x2 - self.x1)/d
            
        V1, s1,c1 = rectToMagDir(self.obj1.vx,self.obj1.vy)
        V2, s2,c2 = rectToMagDir(self.obj2.vx,self.obj2.vy)
        V1Along, V1Normal = resolveComponents(V1, (self.sintheta*c1 - self.costheta*s1), (self.costheta*c1 + self.sintheta*s1))
        V2Along, V2Normal = resolveComponents(V2, (self.sintheta*c2 - self.costheta*s2), (self.costheta*c2 + self.sintheta*s2))
        netRelV = (V1Along - V2Along)
        
        self.obj1.exert((self.k*self.disp - netRelV*self.damp)*self.costheta,(self.k*self.disp - netRelV*self.damp)*self.sintheta,self.obj1)
        self.obj2.exert(-(self.k*self.disp - netRelV*self.damp)*self.costheta,-(self.k*self.disp - netRelV*self.damp)*self.sintheta,self.obj2)
         
    def draw(self): 
        w = 0.25
        x = [self.x1]
        y = [self.y1]
        px = (self.x2 - self.x1)/self.turns
        py = (self.y2 - self.y1)/self.turns
        for i in range(self.turns - 1):
            x.append(self.x1 + (i+1)*px + w*self.sintheta*((-1)**i))
            y.append(self.y1 + (i+1)*py + w*self.costheta*((-1)**i))
        x.append(self.x2)
        y.append(self.y2)
        for i in range(len(x)-1):
            pygame.draw.line(win,(0,0,0),
                             (center[0]+int(simScale*x[i]),center[1] - int(simScale*y[i])),
                             (center[0]+int(simScale*x[i+1]),center[1] - int(simScale*y[i+1])))
            
def get_dist(x1,y1,x2,y2): 
    return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

def sign(x):
    return x/abs(x)

def pseudoString(o1,o2,pulleyLoc1,pulleyLoc2,length): # call this right before evalForces!!
    global rateOfTime    
    T = 0    
    ctr = 0 
    dist1 = get_dist(o1.x,o1.y,pulleyLoc1[0],pulleyLoc1[1])
    dist2 = get_dist(o2.x,o2.y,pulleyLoc2[0],pulleyLoc2[1])
    O1Pcap = -(o1.x - pulleyLoc1[0])/dist1,-(o1.y - pulleyLoc1[1])/dist1
    O2Pcap = -(o2.x - pulleyLoc2[0])/dist2,-(o2.y - pulleyLoc2[1])/dist2
    if dist1 < 1:
        rateOfTime = 0.01
    print(dist1 + dist2)
    if dist1 + dist2 >= length:
        F1x = 0
        F1y = 0
        F2x = 0
        F2y = 0
        
        for f in o1.forces:
            F1x += f[0]
            F1y += f[1] 
        for f in o2.forces:
            F2x += f[0]
            F2y += f[1]  
        F1 = F1x*O1Pcap[0] + F1y*O1Pcap[1]
        F2 = F2x*O2Pcap[0] + F2y*O2Pcap[1]
        #print(F1,F2)
        T = -(F1 + F2)/2
        dist1 = get_dist(o1.x,o1.y,pulleyLoc1[0],pulleyLoc1[1])
        dist2 = get_dist(o2.x,o2.y,pulleyLoc2[0],pulleyLoc2[1])
        while dist1 + dist2 > length + 1 and dt > 0:
            dist1 = get_dist(o1.x,o1.y,pulleyLoc1[0],pulleyLoc1[1])
            dist2 = get_dist(o2.x,o2.y,pulleyLoc2[0],pulleyLoc2[1])
            o1.x += O1Pcap[0]/10*dt; o1.y += O1Pcap[1]/10*dt
            o2.x += O2Pcap[0]/10*dt; o2.y += O2Pcap[1]/10*dt
            ctr+=1 
        #print(T) 
    pygame.draw.circle(win,(0,0,0),(center[0]+int(simScale*((pulleyLoc1[0]+pulleyLoc2[0])/2)),
                                      center[1]-int(simScale*(pulleyLoc1[1]+pulleyLoc2[1])/2)),20,1)
    pygame.draw.line(win,(0,0,0),(center[0]+int(simScale*(o1.x+o1.size/2)),center[1] - int(simScale*o1.y)),
                                 (center[0]+int(simScale*pulleyLoc1[0]),center[1] - int(simScale*pulleyLoc1[1])))
    pygame.draw.line(win,(0,0,0),(center[0]+int(simScale*(o2.x+o1.size/2)),center[1] - int(simScale*o2.y)),
                                 (center[0]+int(simScale*pulleyLoc2[0]),center[1] - int(simScale*pulleyLoc2[1])))
    
    
    o1.exert(T*O1Pcap[0],T*O1Pcap[1],o1)
    o2.exert(T*O2Pcap[0],T*O2Pcap[1],o2)
    print(ctr)
    
    positionArray.append(pygame.time.get_ticks()*rateOfTime*0.001)
    #positionArray.append(T)
        
    
def rule(a,b,v):
    a.vx = v*(b.x - a.x)/get_dist(a.x,a.y,b.x,b.y)
    a.vy = v*(b.y - a.y)/get_dist(a.x,a.y,b.x,b.y)

run = True
simScale = 38 

#a1 = Object(0,0,10000000,1)
a = Object(-5,0,10000,1)
b = Object(5,0,6.9,1)
c = Object(0,17.32/2,0.5,1)

#d = Object(12,-0,0.5,1)
spring3 = Spring(a,c,5,20,1,0)
spring1 = Spring(a,b,5,20,10,0)
spring2 = Spring(b,c,5,20,10,0)

#ground = Object(-15000,-10,100000,100000)
ground = Object(-10,-100,1000000,15)

positionArray = []
positionArray1 = []
for t in range(3141):
    positionArray1.append(10*math.cos(3.14159/2 + t/500.0)*2.718**(-t/(500.0*math.sqrt(3))))
    positionArray1.append(17.32/3 + 10*math.sin(3.14159/2 + t/500.0)*2.718**(-t/(500.0*math.sqrt(3))))
rateOfTime = 0 #ensures approximately 1s per real life second
frames = 0

t0 = tf
tf = pygame.time.get_ticks() 
dt = (tf - t0)*0.001*rateOfTime
oneMoreTimer = pygame.time.get_ticks()
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    win.fill((255,255,255))
    
    
    
    
    k = pygame.key.get_pressed()
    if k[pygame.K_d]:
        a.exert(10,0,a)
    if k[pygame.K_a]:
        a.exert(-10,0,a)
    if k[pygame.K_w]:
        a.exert(0,10,a)
    if k[pygame.K_s]:
        a.exert(0,-10,a)
    if k[pygame.K_SPACE]:
        a.exert(0,100,a)
   
    if k[pygame.K_m]:
        rateOfTime = 10 #not recommended, highly error prone, often violates energy conservation
    if k[pygame.K_n]:
        rateOfTime = 1 # recommended, works really well
    if k[pygame.K_q]:
        rateOfTime = 0.1 # most accurate, slowest, use for slow mo 
    
    if k[pygame.K_RIGHT]:
        center[0] -= 0.1*simScale
    if k[pygame.K_LEFT]:
        center[0] += 0.1*simScale
    if k[pygame.K_UP]:
        center[1] += 0.1*simScale
    if k[pygame.K_DOWN]:
        center[1] -= 0.1*simScale
    
    if k[pygame.K_x]:
        simScale*=1.01
        center[0] = screenCenter[0] - int((screenCenter[0] - center[0])*1.01)
        center[1] = screenCenter[1] - int((screenCenter[1] - center[1])*1.01)
    if k[pygame.K_c]:
        simScale*=0.99
        center[0] = screenCenter[0] - int((screenCenter[0] - center[0])*0.99)
        center[1] = screenCenter[1] - int((screenCenter[1] - center[1])*0.99)
    
    for i in range(10):
        t0 = tf
        tf = pygame.time.get_ticks() 
        dt = (tf - t0)*0.001*rateOfTime
    
        g(a,-10)
        #g(b,-10)
        #g(c,-10)     
        #g(d,-10)
           
        spring1.evalForces()
        spring2.evalForces()
        spring3.evalForces()
        #pseudoString(a, b, [5,1], [5,1], 10)
        a.evalForces()
        b.evalForces()
        c.evalForces()
        #rule(a,b,0.1)
        #rule(b,c,0.1)
        #rule(c,a,0.1)
        #d.evalForces()
        ground.evalForces() 
        
        #positionArray.append(c.x)
        #positionArray.append(c.y)
        
     
    ### if u need tracer
    
    ''' i = 0
    for j in range(len(positionArray)//2-1):
        pygame.draw.line(win,(0,0,0),
                         (center[0]+int(simScale*positionArray[i]),center[1]-int(simScale*positionArray[i+1])),
                         (center[0]+int(simScale*positionArray[i+2]),center[1]-int(simScale*positionArray[i+3])),2)
        i+=2
    i = 0
    for j in range(len(positionArray1)//2-1):
        pygame.draw.line(win,(255,0,0),
                         (center[0]+int(simScale*positionArray1[i]),center[1]-int(simScale*positionArray1[i+1])),
                         (center[0]+int(simScale*positionArray1[i+2]),center[1]-int(simScale*positionArray1[i+3])),2)
        i+=2
      '''
    
    ###
    
    ''' a.draw()
    b.draw()
    c.draw()
    #d.draw()
    spring1.draw()
    spring2.draw()
    spring3.draw()'''
    ground.draw()
    #pygame.draw.circle(win,(0,0,0),(center[0]+int(simScale*((a.x+b.x)/2)),
     #                                 center[1]-int(simScale*(a.y+b.y)/2)),20)
    frames += 1
    '''f = open("C:\\PythonStuff3\\fileGrapher\\firstData6.gff",'w')
    for x in positionArray: 
        f.write(str(x)) 
        f.write('\n')
    f.write('e')
    f.close()
    '''
    
    clock.tick(6000)
    '''if pygame.time.get_ticks() % 1000 == 1:
        print(frames*1000/(pygame.time.get_ticks() - oneMoreTimer))
        frames = 0
        oneMoreTimer = pygame.time.get_ticks()''' #use if u need FPS counter
    pygame.display.update()     

pygame.quit()
sys.exit()       