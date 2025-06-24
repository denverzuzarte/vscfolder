# finding the largest island
import random
import pandas as pd;
# first making the island
n=3;
m=3;
island=[];
i=0;
while(i<n):
    j=0;
    island.append([]);
    while(j<m):
        island[i].append(random.randint(0,1));
        j=j+1;
    i=i+1;
he=pd.DataFrame(island);
print(he);
def search(x,y):
    if (island[x+1][y]%5!=0):
        print("down");
        island[x+1][y]=island[x+1][y]*2;
        if (x+1<n-1):
                search(x+1,y)
    if (island[x][y+1]%7!=0):
        print("right");
        island[x][y+1]=island[x][y+1]*3;
        if (y+1<m-1):
            search(x,y+1)
    if (island[x-1][y]%2!=0):
        print("up");
        island[x-1][y]=island[x-1][y]*5;
        if (0<x-1):
                search(x-1,y)
    if (island[x][y-1]%3!=0):
        print("left");
        island[x][y-1]=island[x][y-1]*7;
        if (0<y-1):
            search(x,y-1)
    else :
        return 0;

i=1;
while(i<n-1):
    j=1;
    while(j<m-1):
        if(island[i][j]==0 and i<n-1 and i>0 and j<m-1 and j>0):
            island[i][j]=1;
            #search function
            search(i,j);
            island[i][j]=0;
        j=j+1;
    i=i+1;
print("");
print (pd.DataFrame(island));