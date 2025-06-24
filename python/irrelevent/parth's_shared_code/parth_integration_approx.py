import math
import pygame,sys
from pygame.locals import *

w,h = 800,600
win = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
win.fill((255,255,255))

xScale = 50
yScale = 50
xcentre = 400
ycentre = 300
screenCentre = (w//2,h//2)
def area(fx,fxplus1,dx,total=False):
    if total:
        return abs(0.5*(fx + fxplus1)*dx)
    else:
        return 0.5*(fx + fxplus1)*dx

#this is where you put the function u wanna graph/integrate

#for trigo functions use math.sin,etc.
def a(x):
    #a = 9
    #return (x*x)**(1/3) + 0.9*(math.sqrt(8 - x*x))*math.sin(3.14159*x*a)  #i haven't set any exception for division by 0, so it may crash
    return math.sin(x)
    
def b(x):
    return x#if any need to plot 2nd function

def e(x):
    return 4#if any need to plot 2nd function

def d(x):
    m = 100000000
    return 4 - 4*m + m*x #if any need to plot 2nd function

def c(x,y):
    if (x*x + y*y - 4)**3 < 4*x*x*y*y*y:
        return True
    else:
        return False

def integrate(function, a, b,total=False): #try to keep b > a, total toggle for if u want total or net area
    area1 = 0
    dx = (b-a)*0.000001# set accuracy by decreasing dx, but depends on your computing power(zyada todna mat :) )
    x = a
    while x <= b:
        area1 += area(function(x),function(x+dx),dx,total)
        x+=dx
    return area1

def graph(x,fx,dx,col):
    if ycentre-int(fx*yScale) > 2000:
        pygame.draw.line(win,col,(xcentre+int(x*xScale),2000),(xcentre+int(x*xScale),ycentre))
    elif ycentre-int(fx*yScale) < -2000:
        pygame.draw.line(win,col,(xcentre+int(x*xScale),-2000),(xcentre+int(x*xScale),ycentre))
    else:
        pygame.draw.line(win,col,(xcentre+int(x*xScale),ycentre-int(fx*yScale)),(xcentre+int(x*xScale),ycentre))
    
def lineGraph(x,fx,fxplusone,dx,col):
    yfinal1 = ycentre-int(fx*yScale)
    yfinal2 = ycentre-int(fxplusone*yScale)
    if yfinal1>2000:
        yfinal1 = 2000
    elif yfinal1<-2000:
        yfinal1 = -2000
    if yfinal2>2000:
        yfinal2 = 2000
    elif yfinal2<-2000:
        yfinal2 = -2000
    pygame.draw.line(win,col,(xcentre+int(x*xScale),yfinal1),(xcentre+int((x+dx)*xScale),yfinal2))

def drawGraph(function,aa,bb,col):
    dx = (bb-aa)*0.0005 # increase dx if experience too low framerate, python is slow and my coding sucks :(
    x = aa
    while x <= bb:
        #graph(x,function(x),dx) # if wanna shade the area under graph
        lineGraph(x,function(x),function(x+dx),dx,col) # if u only wanna draw grpah outline, comment whatever you don't want
        x+=dx
        
def drawInequality(function, xa,xb,ya,yb,col):
    dx = (xb - xa)*0.001
    dy = (yb - ya)*0.001
    x = xa
    y = ya
    while x<xb:
        while y<yb:
            if function(x,y):
                win.set_at((xcentre+int(x*xScale),ycentre-int(y*yScale)),col)
            y+=dy
        y = ya
        x+=dx
    print('done')

def drawEverything():
    pygame.draw.line(win,(255,0,0),(xcentre-1000000,ycentre),(xcentre+1000000,ycentre),2)
    pygame.draw.line(win,(255,0,0),(xcentre,ycentre-1000000),(xcentre,ycentre+1000000),2)
    if inEq:
        drawInequality(c, -10, 10, -10, 10, (255,0,0))
    else:
        pygame.draw.line(win,(255,0,0),(xcentre-1000000,ycentre),(xcentre+1000000,ycentre),2)
        pygame.draw.line(win,(255,0,0),(xcentre,ycentre-1000000),(xcentre,ycentre+1000000),2)
        drawGraph(a,0,6.29,(255,0,0))
        drawGraph(b,-4,4,(0,0,0)) #if any need to plot 2nd function
        drawGraph(e,3.7,4,(0,0,0)) #if any need to plot 3rd function
        drawGraph(d,4-(0.3/100000000),4,(0,0,0)) #if any need to plot 2nd function
def readFromFile(path):
    arr = []
    f = open(path,'r')
    while True:
        l = f.readline()
        if l == 'e':
            break
        arr.append(float(l))
    f.close()
    return arr
    
def graphFromFile(path,colour):
    arr = readFromFile(path)
    x = 0
    y = 1
    for i in range(len(arr)//2 - 1):
        pygame.draw.line(win,colour,(xcentre + int(xScale*arr[x]),ycentre - int(yScale*(arr[y]))),
                         (xcentre + int(xScale*arr[x+2]),ycentre - int(yScale*(arr[y+2]))),2)
        x+=2
        y+=2
    pygame.draw.line(win,colour,(xcentre-1000000,ycentre),(xcentre+1000000,ycentre))
    pygame.draw.line(win,colour,(xcentre,ycentre-1000000),(xcentre,ycentre+1000000))
        


run = True
inEq = False
drawEverything()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            xcentre,ycentre = event.pos
            win.fill((255,255,255))
            drawEverything()
    k = pygame.key.get_pressed()
    if k[pygame.K_UP]:
        win.fill((255,255,255))
        ycentre+=10
        drawEverything()
    if k[pygame.K_DOWN]:
        win.fill((255,255,255))
        ycentre-=10
        drawEverything()
    if k[pygame.K_RIGHT]:
        win.fill((255,255,255))
        xcentre-=10
        drawEverything()
    if k[pygame.K_LEFT]:
        win.fill((255,255,255))
        xcentre+=10
        drawEverything() 
    if k[pygame.K_SPACE]:
        win.fill((255,255,255))
        xScale*=1.02
        yScale*=1.02
        xcentre = screenCentre[0] - int((screenCentre[0] - xcentre)*1.02) 
        ycentre = screenCentre[1] - int((screenCentre[1] - ycentre)*1.02)
        drawEverything()
    if k[pygame.K_c]:
        win.fill((255,255,255))
        xScale*=0.98
        yScale*=0.98
        xcentre = screenCentre[0] - int((screenCentre[0] - xcentre)*0.98) 
        ycentre = screenCentre[1] - int((screenCentre[1] - ycentre)*0.98)
    if k[pygame.K_LCTRL]:
        win.fill((255,255,255))
        xScale*=0.98
        xcentre = screenCentre[0] - int((screenCentre[0] - xcentre)*0.98) 
        #ycentre = screenCentre[1] - int((screenCentre[1] - ycentre)*0.98)
    if k[pygame.K_RCTRL]:
        win.fill((255,255,255))
        yScale*=0.98
       # xcentre = screenCentre[0] - int((screenCentre[0] - xcentre)*0.98) 
        ycentre = screenCentre[1] - int((screenCentre[1] - ycentre)*0.98)
    if k[pygame.K_LSHIFT]:
        win.fill((255,255,255))
        xScale*=1.01
        xcentre = screenCentre[0] - int((screenCentre[0] - xcentre)*0.98) 
        #ycentre = screenCentre[1] - int((screenCentre[1] - ycentre)*0.98)
    if k[pygame.K_RSHIFT]:
        win.fill((255,255,255))
        yScale*=1.01
        #xcentre = screenCentre[0] - int((screenCentre[0] - xcentre)*0.98) 
        ycentre = screenCentre[1] - int((screenCentre[1] - ycentre)*0.98)
    
        drawEverything()
    drawEverything()
    #graphFromFile('C:\\PythonStuff3\\fileGrapher\\firstData6.gff',(255,0,0))
   # graphFromFile('C:\\PythonStuff3\\fileGrapher\\firstData3.gff',(0,255,0))
    #graphFromFile('C:\\PythonStuff3\\fileGrapher\\firstData2.gff',(0,0,255))
    #graphFromFile('C:\\PythonStuff3\\fileGrapher\\firstData1.gff',(255,255,0))
    #graphFromFile('C:\\PythonStuff3\\fileGrapher\\firstData.gff',(0,0,0))
    
    clock.tick(60)
    pygame.display.update()
pygame.quit()
def nice(x):
    return (math.sin(x))**2/(math.sin(x) + math.cos(x))
print(integrate(nice,0,3.14159/2))
