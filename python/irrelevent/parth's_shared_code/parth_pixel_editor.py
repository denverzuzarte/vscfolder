import pygame,sys,math,random
from pygame.locals import *

pixel_number = 8

pygame.init()
win = pygame.display.set_mode((1000//2,1400//2))
pygame.display.set_caption('pixel art editor')
clock = pygame.time.Clock()

def drawGrid():
    inv = (1000//2)//pixel_number
    for x in range(pixel_number+1):
        pygame.draw.line(win,(0,0,0),(0,x*inv),(1000//2,x*inv))
    for y in range(pixel_number+1):
        pygame.draw.line(win,(0,0,0),(y*inv,0),(y*inv,1000//2))
        
def saveToFile(squares,name,path='D:/PythonStuff3'):
    path = path+'/'+name
    f = open(path,'w')
    f.write(str(pixel_number)+'\n')
    for square in squares:
        for s in square:
            string = str(s[0])+' '+str(s[1])+' '+str(s[2])+' '+str(s[3])+' '+str(s[4])+'\n'
            f = open(path,'a')
            f.write(string)
    f.close()
    
def load(path):
    global pixel_number
    f = open(path,'r')
    pixel_number = int(f.readline())
    square = []
    for x in f:
        l = x.split()
        l = [int(l[0]),int(l[1]),int(l[2]),int(l[3]),int(l[4])]
        square.append(l)
    squares = [[0 for x in range(pixel_number)] for y in range(pixel_number)]
    for x in range(pixel_number**2):
        squares[x//pixel_number][x%pixel_number] = square[x]
    return squares
    f.close()
    
class scrollBar:
    def __init__(self,h):
        self.rectpos = 305
        self.h = h
        
    def update(self):
        pygame.draw.rect(win,(0,0,0),(50,self.h,255,10),2)
        if abs(mouse[1] - self.h) < 10 and mouse[0] < 306 and mouse[0] > 49:
            self.rectpos = mouse[0]
        pygame.draw.rect(win,(0,0,0),(self.rectpos,self.h,20,20))
        
    
def random1(squares):
    for square in squares:
        for s in square:
            s[0],s[1],s[2] = random.randint(0,255),random.randint(0,255),random.randint(0,255)
    return squares

run = True
mouse = (10,10)

squares = [[[255,255,255,y,x] for x in range(pixel_number)] for y in range(pixel_number)]

o1 = scrollBar(550)
o2 = scrollBar(600)
o3 = scrollBar(650)
m = pygame.mouse.get_pressed()
squares = load('C:/Users/Denver Zuzarte/.vscode/chessBoard.parth')
inv = 500//pixel_number
#squares = random1(squares)
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            if abs(event.pos[0] - 475) < 25 and abs(event.pos[1] - 550) < 25:
                saveToFile(squares,'pandubabadrawing.parth')
            
        
    m = pygame.mouse.get_pressed()
    win.fill((255,255,255))
    #squares = random1(squares)
    #((o1.rectpos-100)//2,(o2.rectpos-100)//2,(o3.rectpos-100)/2)
    m = pygame.mouse.get_pressed()
    if m[0]:
        mouse = pygame.mouse.get_pos()
        if mouse[1]<500:
            squares[mouse[0]//inv][mouse[1]//inv][0],squares[mouse[0]//inv][mouse[1]//inv][1],squares[mouse[0]//inv][mouse[1]//inv][2] = (o1.rectpos-50),(o2.rectpos-50),(o3.rectpos-50)  
    for square in squares:
        for s in square:
            pygame.draw.rect(win,(s[0],s[1],s[2]),(s[3]*inv,s[4]*inv,inv,inv))
    if pixel_number < 101:
       drawGrid()
       pass
    o1.update()
    o2.update()
    o3.update()
    pygame.draw.rect(win,((o1.rectpos-50),(o2.rectpos-50),(o3.rectpos-50)),(400,550,25,25));pygame.draw.rect(win,(0,0,0),(400,550,25,25),5)
    pygame.draw.rect(win,(0,255,0),(450,550,25,25));pygame.draw.rect(win,(0,0,0),(450,550,25,25),5)
    clock.tick(60)
    pygame.display.update()
#saveToFile(squares,'somethingelse.parth')
pygame.quit()
sys.exit()