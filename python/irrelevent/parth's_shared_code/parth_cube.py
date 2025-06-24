
import pygame,sys,math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

pygame.init()
clock = pygame.time.Clock()
w = 500
h = 500
x = 1

white=(1,1,1)
yellow=(1,1,0)
blue=(0,0,1)
green=(0,1,0)
red=(1,0,0)
orange=(1,0.64,0)

pygame.display.set_mode((w,h), DOUBLEBUF|OPENGL)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(45,(w/h),0.1,50.0)
glMatrixMode(GL_MODELVIEW)  
glTranslatef(0,0,-10)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

def rotationMatrixConstructor(angle,axis):
    if axis == 'x':
        rotationMatrix = [[1,                            0,                             0],
                          [0,math.cos(math.radians(angle)),-math.sin(math.radians(angle))],
                          [0,math.sin(math.radians(angle)), math.cos(math.radians(angle))]]
    elif axis == 'y':
        rotationMatrix = [[math.cos(math.radians(angle)), 0,math.sin(math.radians(angle))],
                          [0,                         1,                        0],
                          [-math.sin(math.radians(angle)),0,math.cos(math.radians(angle))]]
    elif axis == 'z': 
        rotationMatrix = [[math.cos(math.radians(angle)),-math.sin(math.radians(angle)),0],
                          [math.sin(math.radians(angle)),math.cos(math.radians(angle)), 0],
                          [0,                        0,                         1]]
    elif axis == 'none':
        rotationMatrix = [[1,0,0],
                          [0,1,0],
                          [0,0,1]]
    
    return rotationMatrix


def multMatrix(m11,m22):
    m1 = np.array(m11,dtype=np.float32)
    m2 = np.array(m22,dtype = np.float32)
    productMatrix = []
    if len(m1[0]) == len(m2):
        for i in range(len(m1)):
            dotproduct = []
            for j in range(len(m2[0])):
                sum = 0
                for k in range(len(m2)):
                    sum+=(m1[i][k]*m2[k][j])    
                dotproduct.append(sum)
            productMatrix.append(dotproduct)
        return productMatrix
    else:
        return ["no","pe"]

def solidCube(vertices,matrix):
    '''x = center[0]
    y = center[1] 
    z = center[2]'''
    col = 0
    edges = ((0,1),(1,2),(0,3),(2,3),(4,5),(5,6),(6,7),(4,7),(0,4),(1,5),(2,6),(3,7))
    faces = ((0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,4,7,3),(1,5,6,2))
    colors = (blue,green,red,orange,yellow,white)
    newVerticesList = []
    for vertex in vertices:
        vertMat = [[vertex[0]],
                   [vertex[1]],
                   [vertex[2]]]
        newMat = multMatrix(matrix,vertMat)
        newVerticesList.append((newMat[0][0],newMat[1][0],newMat[2][0]))
    vertices = tuple(newVerticesList)
    glBegin(GL_QUADS)
    for face in faces:
        glColor3fv(colors[col])
        col+=1
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0,0,0))
            glVertex3fv(vertices[vertex])
    glEnd()
    return vertices

def cubeList():
    verticesSet = []
    for z in range(-1,2):
        for x in range(-1,2):
            for y in range(-1,2):
                coords = [[x],
                          [y],
                          [z]]
            
                xx = coords[0][0]
                y = coords[1][0]
                z = coords[2][0]
                vertices = ((xx-0.49,y-0.49,z-0.49),(xx+0.49,y-0.49,z-0.49),(xx+0.49,y+0.49,z-0.49),(xx-0.49,y+0.49,z-0.49),(xx-0.49,y-0.49,z+0.49),(xx+0.49,y-0.49,z+0.49),(xx+0.49,y+0.49,z+0.49),(xx-0.49,y+0.49,z+0.49))
                verticesSet.append(vertices)
    return verticesSet

def L():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (0,1,2,9,10,11,18,19,20):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(10,'x'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[18],verticesSet[9],verticesSet[0],verticesSet[3],verticesSet[4],
                   verticesSet[5],verticesSet[6],verticesSet[7],verticesSet[8],verticesSet[19],
                   verticesSet[10],verticesSet[1],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[17],verticesSet[20],verticesSet[11],
                   verticesSet[2],verticesSet[21],verticesSet[22],verticesSet[23],verticesSet[24],
                   verticesSet[25],verticesSet[26]]
            
def R():
    for x in range(2):
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (6,7,8,15,16,17,24,25,26):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(-45,'x'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[2],verticesSet[3],verticesSet[4],
                   verticesSet[5],verticesSet[8],verticesSet[17],verticesSet[26],verticesSet[9],
                   verticesSet[10],verticesSet[11],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[7],verticesSet[16],verticesSet[25],verticesSet[18],verticesSet[19],
                   verticesSet[20],verticesSet[21],verticesSet[22],verticesSet[23],verticesSet[6],
                   verticesSet[15],verticesSet[24]]

def Lprime():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (0,1,2,9,10,11,18,19,20):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(-10,'x'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[2],verticesSet[11],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[5],verticesSet[6],verticesSet[7],verticesSet[8],verticesSet[1],
                   verticesSet[10],verticesSet[19],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[17],verticesSet[0],verticesSet[9],
                   verticesSet[18],verticesSet[21],verticesSet[22],verticesSet[23],verticesSet[24],
                   verticesSet[25],verticesSet[26]]
            
def Rprime():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (6,7,8,15,16,17,24,25,26):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(10,'x'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[2],verticesSet[3],verticesSet[4],
                   verticesSet[5],verticesSet[24],verticesSet[15],verticesSet[6],verticesSet[9],
                   verticesSet[10],verticesSet[11],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[25],verticesSet[16],verticesSet[7],verticesSet[18],verticesSet[19],
                   verticesSet[20],verticesSet[21],verticesSet[22],verticesSet[23],verticesSet[26],
                   verticesSet[17],verticesSet[8]]

def U():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (2,5,8,11,14,17,20,23,26):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(-10,'y'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]
    
            
def D():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (0,3,6,9,12,15,18,21,24):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(-10,'y'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]

def Uprime():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (2,5,8,11,14,17,20,23,26):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(10,'y'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]
            
def Dprime():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (0,3,6,9,12,15,18,21,24):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(10,'y'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]
    
def F():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (0,1,2,3,4,5,6,7,8):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(10,'z'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]
            
def B():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (18,19,20,21,22,23,24,25,26):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(-10,'z'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]

def Fprime():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:    
                    if event.type == MOUSEMOTION:
                        mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
                #pygame.mouse.set_pos((250,250))
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        glRotatef(mvmt[0],0,1,0)
        glRotatef(mvmt[1],0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (0,1,2,3,4,5,6,7,8):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(-10,'z'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]
            
def Bprime():
    for x in range(9):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        glLoadIdentity()
        glMultMatrixf(viewMatrix)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for i in range(len(verticesSet)):
            if i in (18,19,20,21,22,23,24,25,26):
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(10,'z'))
            else:
                verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))
        clock.tick(100)
        pygame.display.flip()
    verticesSet[:] = [verticesSet[0],verticesSet[1],verticesSet[20],verticesSet[3],verticesSet[4],
                   verticesSet[11],verticesSet[6],verticesSet[7],verticesSet[2],verticesSet[9],
                   verticesSet[10],verticesSet[23],verticesSet[12],verticesSet[13],verticesSet[14],
                   verticesSet[15],verticesSet[16],verticesSet[5],verticesSet[18],verticesSet[19],
                   verticesSet[26],verticesSet[21],verticesSet[22],verticesSet[17],verticesSet[24],
                   verticesSet[25],verticesSet[8]]

verticesSet = cubeList()
mvmt = [0,0]
pygame.mouse.set_pos((250,250))

for x in range(105):
    U()
    L()
    
   
    

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_e:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:    
            if event.type == MOUSEMOTION:
                mvmt[:] = [event.pos[0]-250,event.pos[1]-250]
                #pygame.mouse.set_pos((250,250))
             
    glLoadIdentity()
    glMultMatrixf(viewMatrix)
    #glPushMatrix()
    #glTranslatef(0,0,10)
    glRotatef(mvmt[0],0,1,0)
    glRotatef(mvmt[1],0,0,1)
    #glTranslatef(0,0,-10)
    
    #viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    #glPopMatrix()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    for i in range(len(verticesSet)):
        verticesSet[i] = solidCube(verticesSet[i],rotationMatrixConstructor(1,'none'))   
    clock.tick(100)
    pygame.display.flip()
