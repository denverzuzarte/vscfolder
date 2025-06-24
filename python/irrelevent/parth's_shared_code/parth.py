import pygame, math,sys,random
from pygame.locals import *

pygame.init()
w,h = 800,600
win = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
offset = [0,0]
scale = 10 #DO NOT CHANGE, SET AT START OF PROGRAM! and keep it int

entity_arr = [[False for y in range(100)] for x in range(100)]
change_list = [] #set of coords whose life state to change        

def block(x,y,xsize,ysize):
    for i in range(xsize):
        for j in range(ysize):
            entity_arr[x+i][y+j] = True

def draw(coords,isAlive):
    if isAlive:
        pygame.draw.rect(win,(255,255,255),(coords[0]*scale,coords[1]*scale,scale,scale))
        pygame.draw.rect(win,(0,0,0),(coords[0]*scale + scale*0.1,coords[1]*scale + scale*0.1,scale*0.8,scale*0.8),int(scale*0.9))
        
    else:
        pygame.draw.rect(win,(0,0,0),(coords[0]*scale,coords[1]*scale,scale,scale),1)
        

def check():
    '''
    Any live cell with two or three live neighbours survives.
Any dead cell with three live neighbours becomes a live cell.
All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    
    '''
    for x in range(len(entity_arr)-2):
        for y in range(len(entity_arr)-2):
            ctr = 0
            i = x+1
            j = y+1
            if entity_arr[i+1][j+1]:
                ctr+=1
            if entity_arr[i+1][j]:
                ctr+=1
            if entity_arr[i+1][j-1]:
                ctr+=1
            if entity_arr[i][j+1]:
                ctr+=1
            if entity_arr[i][j-1]:
                ctr+=1
            if entity_arr[i-1][j+1]:
                ctr+=1
            if entity_arr[i-1][j]:
                ctr+=1
            if entity_arr[i-1][j-1]:
                ctr+=1
            if entity_arr[i][j]:
                if ctr == 2 or ctr == 3:
                    pass
                else:
                    change_list.append([i,j])
            if not entity_arr[i][j]:
                if ctr == 3:
                    change_list.append([i,j])
                    
def update():
    global change_list
    for x in change_list:
        entity_arr[x[0]][x[1]] = not entity_arr[x[0]][x[1]]
    change_list = []

#block(20,20,25,25)

started = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and not started:
            gridX = event.pos[0]//scale
            gridY = event.pos[1]//scale
            entity_arr[gridX][gridY] = not entity_arr[gridX][gridY] 
        if event.type == KEYDOWN:
            started = not started
    
    win.fill((255,255,255))
    if started:
        check()
        pygame.time.wait(250)
        update()
    for i in range(len(entity_arr)):
        for j in range(len(entity_arr)):
            draw([i,j],entity_arr[i][j])
    clock.tick(60)
    pygame.display.flip()
    
pygame.quit()
sys.exit()